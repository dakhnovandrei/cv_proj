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
