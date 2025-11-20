FROM ultralytics/ultralytics:latest

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ai_model/ ./ai_model/

RUN mkdir -p output model


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]