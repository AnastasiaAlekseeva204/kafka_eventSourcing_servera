from structure.database import SessionLocal
from structure.student_kafka import StudentEventProducer as KafkaService
from structure.database_models import Student
from structure.student_events import StudentCreated, StudentUpdated, StudentDeleted

# Твои внутренние импорты сервиса
from enrollment.enrollment_saga import request_enrollment
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
async def create_student(
    body: StudentCreate, 
    user_id: int = Depends(get_current_user), 
    session: Session = Depends(get_session) # Добавляем сессию БД
):
    student_id = str(uuid.uuid4())
    
    # 1. Сначала создаем самого студента в его таблице
    new_student = Student(
        id=student_id, # если у тебя UUID как строка
        last_name=body.last_name,
        first_name=body.first_name,
        middle_name=body.middle_name,
        gender=body.gender,
        age=body.age,
        owner_id=user_id
    )
    session.add(new_student)

    # 2.  создаю запись в Outbox
    # Debezium увидит эту запись и САМ отправит её в Kafka
    outbox_event = Outbox(
        aggregate_type="student",
        aggregate_id=student_id,
        type="StudentCreated",
        payload={
            "op": "c",
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
    )
    session.add(outbox_event)
    
    # 3. Фиксируем транзакцию. 
    # Теперь либо сохранятся оба (студент и событие), либо ничего.
    session.commit()
    
    return {"id": student_id, "status": "saved_to_outbox"}

@router.patch("/api/students/{student_id}")
async def update_student(
    student_id: str, 
    body: StudentUpdate, 
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Но для Outbox главное — записать событие "u" (update) в таблицу
    outbox_event = Outbox(
        aggregate_type="student",
        aggregate_id=student_id,
        type="StudentUpdated",
        payload={
            "op": "u",
            "student": {
                "student_id": student_id,
                "owner_id": user_id,
                **body.model_dump(exclude_none=True)
            }
        }
    )
    session.add(outbox_event)
    session.commit()
    return {"status": "update_saved_to_outbox"}

@router.delete("/api/students/{student_id}")
async def delete_student(
    student_id: str, 
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session) # Не забываем сессию
):
    # 1. Сначала удаляем (или помечаем удаленным) студента из основной таблицы
    # student = session.query(Student).filter(Student.id == student_id, Student.owner_id == user_id).first()
    # if student:
    #     session.delete(student)
    
    # 2. Записываем событие удаления в Outbox
    # Debezium увидит операцию "d" и отправит её в Kafka
    outbox_event = Outbox(
        aggregate_type="student",
        aggregate_id=student_id,
        type="StudentDeleted",
        payload={
            "op": "d",  # 'd' = delete (в стиле Debezium)
            "student_id": student_id,
            "user_id": user_id
        }
    )
    
    session.add(outbox_event)
    
    # 3. Фиксируем транзакцию
    session.commit()
    
    return {"message": "Delete event saved to outbox", "student_id": student_id}   