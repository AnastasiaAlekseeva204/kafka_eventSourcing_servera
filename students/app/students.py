import uuid
from dataclasses import asdict
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Union, Any
from http import HTTPStatus
from math import ceil
from sqlalchemy.orm import Session

from database import SessionLocal
from database_models import Student
from validation_models import StudentOut, StudentCreate, StudentUpdate
from fastapi.security import OAuth2PasswordBearer
from crypt import CryptService
from producer import KafkaService
from student_events import StudentCreated, StudentUpdated, StudentDeleted

router = APIRouter()
security = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/api/auth/login")


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_user(token: str = Depends(security)) -> int:
    try:
        user_id = CryptService.decode_token(token)
        if not user_id:
            raise HTTPException(status_code=401, detail="User not found")
        return int(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")


def student_to_dict(student) -> dict:
    return {
        "id": student.id,
        "last_name": student.last_name,
        "first_name": student.first_name,
        "middle_name": student.middle_name,
        "gender": student.gender,
        "age": student.age,
    }


@router.get("/health", status_code=HTTPStatus.OK)
def health():
    return {"status": "ok"}


@router.get("/api/students/{student_id}")
def get_student(student_id: int, user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):
    student = session.query(Student).filter(Student.id == student_id, Student.owner_id == user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_to_dict(student)


@router.post("/api/students/", status_code=201)
async def create_student(body: StudentCreate, user_id: int = Depends(get_current_user)):
    # 1. Генерируем UUID (бизнес-ключ)
    student_id = str(uuid.uuid4())
    
    # 2. Формируем словарь в формате, который ждет StudentEventSourcing (с ключом 'op')
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
    # Для обновления тоже нужен формат с 'op' и 'student'
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
    # Для удаления формат в твоем student_es.py ждет 'op' и 'student_id' напрямую
    event_for_kafka = {
        "op": "d",  # 'd' = delete
        "student_id": student_id,
        "user_id": user_id
    }

    KafkaService.send_message("student-events", event_for_kafka)
    return {"message": "Delete event produced"}