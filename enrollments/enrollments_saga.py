from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import os

# Настройка клиента реестра схем
sr_client = SchemaRegistryClient({'url': os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry:8081")})

# Читаем схему из файла
with open("enrollments/enrollment.avsc") as f:
    schema_str = f.read()

avro_serializer = AvroSerializer(sr_client, schema_str)

def request_enrollment(student_id: str, course_id: str, user_id: int):
    enrollment_id = str(uuid.uuid4())
    event_id = str(uuid.uuid4())
    
    event_payload = {
        "event_id": event_id,
        "op": "enroll_requested",
        "enrollment_id": enrollment_id,
        "student_id": student_id,
        "course_id": course_id,
        "user_id": user_id
    }
    
    # Теперь отправляем через KafkaService, но уже сериализованные данные
    KafkaService.send_message_avro("student-events", event_payload, avro_serializer)
    
    return enrollment_id