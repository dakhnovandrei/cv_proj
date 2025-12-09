FROM ultralytics/ultralytics:latest

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Создаём необходимые директории
RUN mkdir -p /app/model /app/output

# Запуск приложения
CMD ["/bin/bash", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
