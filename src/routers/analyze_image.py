from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session



analyze_router = APIRouter()


@analyze_router.post("/analyze", tags=["Analyze"])
async def analysis():
    ...