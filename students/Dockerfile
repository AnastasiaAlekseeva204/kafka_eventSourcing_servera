# Используем slim версию, она стабильнее alpine для работы с базами данных
FROM python:3.13-slim


#apt-get update: Обновляет списки доступных пакетов.
#apt-get install -y curl: Устанавливает curl (флаг -y автоматически отвечает «да» на вопросы).
#rm -rf /var/lib/apt/lists/*: Удаляет временные файлы кэша, чтобы образ Docker весил меньше (хорошая практика).
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Устанавливаем системные зависимости для работы с PostgreSQL (если используешь psycopg2)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Копируем файл зависимостей
COPY app/requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn "uvicorn[standard]"
# Копируем все файлы приложения
COPY app/*.py ./

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "1", "main:app"]