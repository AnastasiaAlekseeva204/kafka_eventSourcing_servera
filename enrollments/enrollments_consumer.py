import os
from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from .database import SessionLocal
from .models import ProcessedEvent
from .enrollment_saga import confirm_enrollment

# 1. Настройка Schema Registry Client
# URL берем из переменных окружения (обычно http://schema-registry:8081)
sr_url = os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry:8081")
sr_client = SchemaRegistryClient({'url': sr_url})

# 2. Создаем десериализатор
# Он будет автоматически скачивать нужную схему из реестра по ID в заголовке сообщения
avro_deserializer = AvroDeserializer(sr_client)

c = Consumer({
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    "group.id": "enrollment-processor-group",
    "auto_offset_reset": "earliest",
    "enable.auto.commit": "false"
})
c.subscribe(["student_events"])

print("🚀 Обработчик зачислений (Avro + Schema Registry) запущен...")

try:
    while True:
        msg = c.poll(1.0)
        if msg is None: continue
        if msg.error(): continue

        try:
            # ТЕПЕРЬ: Десериализуем сообщение с помощью Avro
            # Если формат сообщения не совпадет со схемой в реестре, тут вылетит ошибка
            event = avro_deserializer(msg.value(), None) 
            
            event_id = event.get("event_id")
            
            with SessionLocal() as session:
                # 1. Проверка на идемпотентность (защита от дублей)
                if session.query(ProcessedEvent).filter_by(event_id=event_id).first():
                    print(f"[*] Skipping already processed event: {event_id}")
                    c.commit(msg)
                    continue

                # 2. Вызов логики Саги
                if event.get("op") == "enroll_requested":
                    confirm_enrollment(session, event)

                # 3. Фиксация события в нашей БД (чтобы не обрабатывать дважды)
                session.add(ProcessedEvent(event_id=event_id))
                session.commit()
                
            # 4. Коммит в Kafka (подтверждаем, что сообщение обработано)
            c.commit(msg)

        except Exception as e:
            # Сюда попадем, если Schema Registry не найдет схему или данные битые
            print(f"❌ Ошибка валидации схемы или обработки: {e}")

finally:
    c.close()