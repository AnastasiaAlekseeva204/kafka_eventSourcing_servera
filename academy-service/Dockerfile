# Внутри academy-service/Dockerfile
FROM python:3.10-slim
WORKDIR /app

COPY academy-service/requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

COPY structure/ ./structure/
COPY enrollments/ ./enrollments/
COPY academy-service/app/ ./app/

ENV PYTHONPATH=/app