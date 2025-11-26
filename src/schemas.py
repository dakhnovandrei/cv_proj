from datetime import datetime
from typing import Optional, Dict, Any, List

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(..., min_length=6, max_length=72)


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class DiseaseResult(BaseModel):
    disease: str = Field(example="leaf_spot")
    recommendation: str = Field(example="Apply fungicide...")


class AnalysisResponse(BaseModel):
    image_url: str = Field(example="https://minio.example.com/bucket/image.jpg")
    results: List[DiseaseResult]


class AnalysisHistoryItem(BaseModel):
    request_id: int = Field(example=123)
    image_url: str = Field(example="https://minio.example.com/bucket/image.jpg")
    created_at: datetime = Field(example="2025-11-25T0:43:10.000Z")
    results: list[DiseaseResult]


class AnalysisHistoryList(BaseModel):
    total: int = Field(example=15, ge=0)
    page: int = Field(example=1, ge=1)
    page_size: int = Field(example=10, ge=1, le=100)
    history: list[AnalysisHistoryItem]
