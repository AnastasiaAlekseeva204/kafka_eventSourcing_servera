from fastapi import FastAPI
import uuid
from dataclasses import asdict
from fastapi import HTTPException, Depends
from typing import List, Optional, Dict, Union, Any
from http import HTTPStatus
from math import ceil
from sqlalchemy.orm import Session

from database import SessionLocal
from database_models import Student
from producer import KafkaService
from student_events import StudentCreated, StudentUpdated, StudentDeleted

# academy запрос делает
#enrollment главный плюс обрабатывает
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "academy service alive"}

@router.get("/api/students/{student_id}")
def get_student(student_id: int, user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):
    student = session.query(Student).filter(Student.id == student_id, Student.owner_id == user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_to_dict(student)


@router.post("/api/students/", status_code=201)
async def create_student(body: StudentCreate, user_id: int = Depends(get_current_user)):
    student_id = str(uuid.uuid4())
    
    event_for_kafka = {
        "op": "c",  # 'c' = create
        "student": {
            "student_id": student_id,
            "last_name": body.last_name,
            "first_name": body.first_name,
            "middle_name": body.middle_name,
            "gender": body.gender,
            "age": body.age,
            "owner_id": user_id
        }
    }
    
    # 3. Отправляем именно event_for_kafka
    KafkaService.send_message("student-events", event_for_kafka)
    
    return {"id": student_id, "status": "created_via_events"}

@router.patch("/api/students/{student_id}")
async def update_student(student_id: str, body: StudentUpdate, user_id: int = Depends(get_current_user)):
    event_for_kafka = {
        "op": "u",  # 'u' = update
        "student": {
            "student_id": student_id,
            "owner_id": user_id,
            **body.model_dump(exclude_none=True)
        }
    }
    
    KafkaService.send_message("student-events", event_for_kafka)
    return {"status": "update_event_produced"}

@router.delete("/api/students/{student_id}")
async def delete_student(student_id: str, user_id: int = Depends(get_current_user)):
    event_for_kafka = {
        "op": "d",  # 'd' = delete
        "student_id": student_id,
        "user_id": user_id
    }

    KafkaService.send_message("student-events", event_for_kafka)
    return {"message": "Delete event produced"}    