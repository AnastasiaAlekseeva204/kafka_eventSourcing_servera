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
        consumer_timeout_ms=3000, # Увеличим до 3 секунд для надежности
        value_deserializer=lambda b: json.loads(b.decode()),
        group_id=None # Важно: читаем как независимый консьюмер
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
        op = event.get("op")
        
        # Пытаемся найти ID везде, где он может быть
        curr_id = event.get("student_id") or event.get("student", {}).get("student_id")
        
        # Приводим к строке, чтобы избежать проблем сравнения UUID и str
        if str(curr_id) == str(student_id):
            found = True  # МЫ НАШЛИ СОБЫТИЕ!
            if op == "d":
                state["deleted"] = True
            else:
                student_data = event.get("student", {})
                state.update(student_data)
                state["deleted"] = False
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