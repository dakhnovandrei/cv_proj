FROM ultralytics/ultralytics:latest

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/alembic.ini .
# Копируем проект
COPY . .

# Создаём необходимые директории
RUN mkdir -p /app/model /app/output

# Запуск приложения
CMD ["/bin/bash", "-c", "export PYTHONPATH=/app/backend:$PYTHONPATH && alembic upgrade head && uvicorn src.main:app --app-dir /app/backend/src --host 0.0.0.0 --port 8000"]
