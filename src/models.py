import enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, JSON, ForeignKey, Float, Text
import datetime

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user_request = relationship("UserRequests", back_populates="user")
    analysis = relationship("Analysis", back_populates="user")


class UserRequests(Base):
    __tablename__ = "user_requests"

    request_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    image = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())

    user = relationship("Users", back_populates="user_request")
    response = relationship("ModelResponse", back_populates="request")


class ModelResponse(Base):
    __tablename__ = "model_response"

    response_id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("user_requests.request_id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())

    analysis = relationship("Analysis", back_populates="response")
    request = relationship("UserRequests", back_populates="response")


class Analysis(Base):
    __tablename__ = "analysis"

    analysis_id = Column(Integer, primary_key=True, index=True)
    processed_image = Column(String, nullable=False)
    disease_id = Column(Integer, ForeignKey("diseases.disease_id"))
    confidence = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())

    response = relationship("ModelResponse", back_populates="analysis")
    disease = relationship("Diseases", back_populates="analysis")


class Diseases(Base):
    __tablename__ = "diseases"

    disease_id = Column(Integer, primary_key=True, index=True)
    disease_name = Column(String(50), nullable=False)
    recommendation = Column(Text, nullable=False)

    analysis = relationship("Analysis", back_populates="disease")
