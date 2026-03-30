import json
import os
from confluent_kafka import Consumer
from app.database import SessionLocal
from app.models import ProcessedEvent, Enrollment 
from app.enrollment_saga import confirm_enrollment, cancel_enrollment

KAFKA_CONF = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    "group.id": "academy-enrollment-service",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": "false"
}

c = Consumer(KAFKA_CONF)
c.subscribe(["student_creations"])
print("🚀 Enrollments Consumer started. Waiting for events...")

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        try:
            event = json.loads(msg.value().decode("utf-8"))
            event_id = event.get("event_id") 
            student_id = event.get("student_id")

            with SessionLocal() as session:
                if session.query(ProcessedEvent).filter(ProcessedEvent.event_id == event_id).first():
                    print(f"[*] Event {event_id} already processed. Skipping.")
                    c.commit(msg)
                    continue

                # 2. Логика Саги 
                if event["op"] == "EnrollmentApproved":
                    # Если места на курсе есть/условия соблюдены
                    confirm_enrollment(session, student_id)
                elif event["op"] == "EnrollmentDenied":
                    # Если мест нет или студент не подходит
                    cancel_enrollment(session, student_id)
                
                # Дополнительно: если ты используешь промежуточный статус (Requested)
                elif event["op"] == "enroll_requested":
                    # Можно вызвать логику проверки здесь или в отдельном сервисе
                    print(f"[*] New enrollment request for {student_id}")

                # 3. Сохраняем факт обработки события
                session.add(ProcessedEvent(event_id=event_id))
                session.commit()
                print(f"✅ Successfully processed {event['op']} for student {student_id}")

        except Exception as e:
            print(f"Error processing message: {e}")
            # Здесь можно добавить логику записи в Dead Letter Queue

        # Подтверждаем прочтение в Kafka только после успешного commit в БД
        c.commit(msg)

except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    c.close()