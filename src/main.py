import sys
import os

sys.path.append(os.path.dirname(__file__))

from database import Base, engine, get_db, SessionLocal as session_local

from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig

from .routers.users import router

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router, prefix='/api/v1', tags=["Users"])


@app.on_event("startup")
def on_startup():
    db = session_local()
    try:
        ...
    finally:
        db.close()
