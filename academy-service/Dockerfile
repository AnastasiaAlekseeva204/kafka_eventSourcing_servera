# Внутри academy-service/Dockerfile
FROM python:3.10-slim
WORKDIR /app

COPY academy-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем папки относительно корня проекта
COPY structure/ ./structure/
COPY enrollments/ ./enrollments/
COPY academy-service/app/ ./app/

ENV PYTHONPATH=/app