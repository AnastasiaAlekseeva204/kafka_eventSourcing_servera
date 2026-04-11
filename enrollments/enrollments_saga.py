from sqlalchemy.orm import Session
from .models import EnrollmentRecord, ProcessedEvent

def confirm_enrollment(session: Session, event: dict):
    # Проверяем, нет ли уже такого зачисления (бизнес-логика)
    existing = session.query(EnrollmentRecord).filter(
        EnrollmentRecord.student_id == event["student_id"],
        EnrollmentRecord.course_id == event["course_id"]
    ).first()

    if not existing:
        # Создаем запись о подтвержденном зачислении
        new_enrollment = EnrollmentRecord(
            student_id=event["student_id"],
            enrollment_id=event["enrollment_id"],
            course_id=event["course_id"],
            status="CONFIRMED"
        )
        session.add(new_enrollment)
        print(f"✅ Enrollment {event['enrollment_id']} confirmed in DB")