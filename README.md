# CV Plant Disease Detector

Проект **CV Plant Disease Detector** предназначен для садоводов и огородников. С помощью этого приложения можно определить заболевания растений по фотографии, что позволяет вовремя принимать меры для защиты урожая. В базе проекта содержится около **30 различных видов болезней**, а модель демонстрирует высокую точность распознавания.

## Основные возможности

- Анализ фотографии растения и определение заболевания.  
- Поддержка большого количества видов болезней (около 30).  
- Удобный веб-интерфейс для быстрого взаимодействия.  
- Высокая точность модели, минимизация ошибок распознавания.

## Установка и запуск

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/dakhnovandrei/cv_proj/tree/main
cd cv_proj
```
2. **Создайте файл .env в корне проекта и добавьте конфиденциальную информацию**:

    Подключение к базе данных PostgreSQL
    
    Secret key для кодировки JWT токенов
    
    Длительность жизни токенов
    
    Настройки для взаимодействия с MinIO
    
    Пример структуры .env:
```
      DATABASE_URL=postgresql+psycopg://user:********@db:5432/name
      POSTGRES_DB=name
      POSTGRES_USER=user
      POSTGRES_PASSWORD=*********
      PGPORT=5432
      SECRET_KEY=your secret key
      ALGORITHM=...
      ACCESS_TOKEN_EXPIRE_MINUTES=15
      REFRESH_TOKEN_EXPIRE_MINUTES=120
      MINIO_ROOT_USER=*****
      MINIO_ROOT_PASSWORD=******
      MINIO_ENDPOINT=minio:9000
      MINIO_PUBLIC_URL=localhost:9000
      MINIO_PORT=9000
      MINIO_ACCESS_KEY=****
      MINIO_SECRET_KEY=******
      BUCKET_NAME=name
```
3. **Запустите проект через докер:**
```
docker-compose up -d --build
```
4. **Откройте веб-приложение в браузере:**
```
http://localhost:3000
```
**Стек технологий:**

    -YOLO (для распознавания болезней)
    
    -FastAPI, SQLAlchemy, Alembic(backend)
    
    -Docker & Docker Compose
    
    -PostgreSQL (для хранения данных)
    
    -MinIO (для хранения загруженных фотографий)
    
    -React, Vite, Tailwind (frontend)
