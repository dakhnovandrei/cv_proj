import logging
import os
import sys

from fastapi import FastAPI
from sqlalchemy import text

from src.database import engine, SessionLocal
from src.routers.users import router
from src.routers.analyze_image import analyze_router
from authx import AuthX, AuthXConfig
from src.models import Base, Users, Analysis, UserRequests, \
    ModelResponse  # обязательно импортируем модели, чтобы их зарегистрировать

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# Настраиваем AuthX
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router, prefix='/api/v1', tags=["Auth"])
app.include_router(analyze_router, prefix='/api/v2', tags=["Analyze"])

logger = logging.getLogger("uvicorn")  # использовать логгер Uvicorn
logger.setLevel(logging.INFO)


@app.on_event("startup")
def on_startup():
    logger.info("Initializing database...")
    logger.info("Tables created (if not exist).")
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database connection successful.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
    finally:
        db.close()
