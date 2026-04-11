FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости именно из папки сервиса
COPY academy-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем общие модули
COPY structure/ ./structure/

# Копируем сам сервис в подпапку app
COPY academy-service/app/ ./app/

# Если в корне academy-service есть еще важные файлы (например, alembic или доп. скрипты), 
# можно скопировать их отдельно, но главное, чтобы структура внутри /app совпадала с импортами