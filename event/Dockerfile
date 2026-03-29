FROM python:3.11-slim
RUN apt-get update && apt-get install -y libpq-dev gcc curl && rm -rf /var/lib/apt/lists/*
RUN pip install fastapi uvicorn kafka-python sqlalchemy psycopg2-binary
WORKDIR /app
COPY app/main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
