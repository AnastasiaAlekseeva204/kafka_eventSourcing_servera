import json
import os
from fastapi import FastAPI, HTTPException
from kafka import KafkaConsumer

app = FastAPI()

def replay(student_id: str) -> dict:
    consumer = KafkaConsumer(
        "student-events",
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        consumer_timeout_ms=1000,
        value_deserializer=lambda b: json.loads(b.decode()),
        # Добавляем group_id=None, чтобы каждый запрос читал историю с начала
        group_id=None 
    )

    state = {
        "student_id": None,
        "user_id": None,
        "last_name": None,
        "first_name": None,
        "middle_name": None,
        "gender": None,
        "age": None,
        "deleted": False,
    }

    found = False
    
    for msg in consumer:
        event = msg.value
        # Важно: в Kafka может лежать 'id' или 'student_id'
        # Из твоего сервиса students летит структура {'student_id': ..., 'student': {...}}
        curr_id = event.get("student_id") or event.get("student", {}).get("student_id")
        
        # Принудительно приводим к строке для надежного сравнения
        if str(curr_id) == str(student_id):
            found = True
            op = event.get("op")
            
            if op == "d":
                state["deleted"] = True
            else:
                student_data = event.get("student", {})
                state.update(student_data)
                state["deleted"] = False
                # Мапим owner_id (из твоей модели) в user_id для фронтенда
                if "owner_id" in student_data:
                    state["user_id"] = student_data["owner_id"]

    consumer.close()
    return state if found else None

@app.get("/api/students/{student_id}")
async def get_student(student_id: str):
    print(f"DEBUG: Received request for ID: {student_id}", flush=True)
    state = replay(student_id)

    if not state:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if state.get("deleted"):
        # 410 Gone — отличный статус для удаленного ресурса в дипломе
        raise HTTPException(status_code=410, detail="Student deleted")

    return state

@app.get("/health")
def health():
    return {"status": "ok"}