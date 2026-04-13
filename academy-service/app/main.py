from structure.database import SessionLocal
from structure.database_models import Student # <--- Проверь, что в database_models.py есть класс Student
from structure.producer import KafkaService
from structure.student_events import StudentCreated, StudentUpdated, StudentDeleted

# Твои внутренние импорты сервиса
from app.enrollment_saga import request_enrollment
from app.validation_models import EnrollmentCreate, EnrollmentOut

# academy запрос делает
#Инициатор (Choreography Starter)
#enrollment главный плюс обрабатывает
app = FastAPI()
router = app

@app.get("/health")
def health():
    return {"status": "academy service alive"}


# НОВЫЙ ЭНДПОИНТ
@app.post("/api/enrollments/", response_model=EnrollmentOut)
async def create_enrollment(body: EnrollmentCreate, user_id: int = Depends(get_current_user)):
    """
    Academy делает запрос на зачисление.
    Это Инициатор (Choreography Starter).
    """
    try:
        # Вызываем логику Саги, которая отправит событие "enroll_requested"
        enrollment_id = request_enrollment(
            student_id=body.student_id, 
            course_id=body.course_id,
            user_id=user_id
        )
        
        # Возвращаем PENDING, так как процесс асинхронный
        return {
            "enrollment_id": enrollment_id, 
            "status": "PENDING"
        }
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
            detail=f"Saga failed to start: {str(e)}"
        )


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