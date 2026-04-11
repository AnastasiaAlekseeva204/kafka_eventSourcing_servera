from sqlalchemy.orm import Session
from .models import EnrollmentRecord, ProcessedEvent

import uuid
from producer import KafkaService

def request_enrollment(student_id: str, course_id: str, user_id: int):
    enrollment_id = str(uuid.uuid4())
    event_id = str(uuid.uuid4()) # Для защиты от дублей (идемпотентность)
    
    event_for_kafka = {
        "event_id": event_id,
        "op": "enroll_requested", # Наша сложная операция
        "enrollment_id": enrollment_id,
        "student_id": student_id,
        "course_id": course_id,
        "user_id": user_id
    }
    
    # Отправляем в тот же топик или в отдельный "enrollment-events"
    KafkaService.send_message("student-events", event_for_kafka)
    
    return enrollment_id