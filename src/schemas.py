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


# class AnalysisBase(BaseModel):
#     analysis_id: int
#     original_image_url: str
#     processed_image_url: Optional[str]
#     status: str
#     created_at: datetime
#     processing_time: Optional[float]
#     detections_summary: Optional[Dict[str, Any]]
#
#
# class AnalysisList(BaseModel):
#     analyses: List[AnalysisBase]
#     total: int
#
# class DetectionResponse(BaseModel):
#     class_name: str
#
#
# class AnalysisResponse(AnalysisBase):
#     detection = List[DetectionResponse]
#
#     class Config:
#         from_attributes = True

class ProccessingRes(BaseModel):
    image_url: str
    detection_count: int
    status: str
