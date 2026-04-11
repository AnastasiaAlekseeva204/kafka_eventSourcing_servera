import json
import os
from confluent_kafka import Consumer
from .database import SessionLocal
from .models import ProcessedEvent
from .enrollment_saga import confirm_enrollment # Импортируем нашу логику

#Обработчик (Choreography Follower)

c = Consumer({
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    "group.id": "enrollment-processor-group",
    "auto_offset_reset": "earliest",
    "enable.auto.commit": "false"
})
c.subscribe(["student_events"])

print("🚀 Enrollment Main Processor is running...")

try:
    while True:
        msg = c.poll(1.0)
        if msg is None: continue
        if msg.error(): continue

        try:
            event = json.loads(msg.value().decode("utf-8"))
            event_id = event.get("event_id")
            
            with SessionLocal() as session:
                # 1. Проверка на идемпотентность
                if session.query(ProcessedEvent).filter_by(event_id=event_id).first():
                    print(f"[*] Skipping already processed event: {event_id}")
                    c.commit(msg)
                    continue

                # 2. Вызов логики Саги
                if event.get("op") == "enroll_requested":
                    confirm_enrollment(session, event)

                # 3. Фиксация события
                session.add(ProcessedEvent(event_id=event_id))
                session.commit()
                
            # 4. Коммит в Kafka
            c.commit(msg)

        except Exception as e:
            print(f"❌ Error in processing message: {e}")
            # Здесь можно добавить логику retry или отправку в error-topic

finally:
    c.close()