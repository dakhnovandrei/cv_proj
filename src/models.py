import enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, JSON, ForeignKey, Float, Text
import datetime

Base = declarative_base()


class AnalysisStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    analysis = relationship("Analysis", back_populates="user")


class TritonModels(Base):
    __tablename__ = "triton_models"

    model_id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50), nullable=False)
    triton_url = Column(String(100), nullable=False)
    config = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())


# table for interaction between triton and our app
class InferenceRequests(Base):
    __tablename__ = "inference_requests"

    request_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    model_id = Column(Integer, ForeignKey("triton_models.model_id"))
    analysis_id = Column(Integer, ForeignKey("analysis.analysis_id"))
    # data for request
    input_shape = Column(JSON)
    input_data_type = Column(String(20))
    preprocessed_image_path = Column(String(500))

    # triton data
    triton_request_id = Column(String(100))
    triton_model_version = Column(String(50))

    # timing and status of request
    status = Column(String(20), default="pending")  # pending, proccessing
    queue_time = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    total_processing_time = Column(Float)

    created_at = Column(DateTime, default=datetime.datetime.utcnow())

    user = relationship("Users")
    model = relationship("TritonModels")
    response = relationship("InferenceResponses", uselist=False, back_populates="request")
    analysis = relationship("Analysis", back_populates="inference_request")


class InferenceResponses(Base):
    __tablename__ = "inference_responses"

    response_id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("inference_requests.request_id"), unique=True)

    # answer from triton
    raw_output = Column(JSON)
    output_shape = Column(JSON)

    # post-processed results
    detection = Column(JSON)
    num_detection = Column(Integer)
    average_confidence = Column(Float)

    # meta-data
    gpu_util = Column(Float)
    memory_used = Column(Float)

    created_at = Column(DateTime, default=datetime.datetime.utcnow())

    request = relationship("InferenceRequests", back_populates="response")


class DetectionResults(Base):
    __tablename__ = "detection_results"

    detection_id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("inference_responses.response_id"))
    disease_id = Column(Integer, ForeignKey('diseases.disease_id'), nullable=False)

    class_id = Column(Integer, nullable=False)
    class_name = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    bbox = Column(JSON, nullable=False)
    bbox_pixels = Column(JSON)

    response = relationship("InferenceResponses")
    disease = relationship("Diseases", back_populates="detection_results")


class Diseases(Base):
    __tablename__ = "diseases"
    disease_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    name_latin = Column(String(200))
    description = Column(Text)
    treatment_recommendation = Column(Text)
    plant_species = Column(String(200))
    severity = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())

    detection_results = relationship("DetectionResults", back_populates="disease")


class Analysis(Base):
    __tablename__ = "analysis"

    analysis_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    original_filename = Column(String(255), nullable=False)
    original_image_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    image_dimensions = Column(JSON)  # {"width": 1920, "height": 1080}

    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.pending)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    completed_at = Column(DateTime)

    user = relationship("Users", back_populates="analysis")
    inference_request = relationship('InferenceRequests', uselist=False, back_populates="analysis")


class ModelPerformance(Base):
    __tablename__ = "model_performance"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("triton_models.model_id"))

    # metrics
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())
    average_latency = Column(Float)
    request_per_sec = Column(Float)
    error_rate = Column(Float)
    gpu_memory_usage = Column(Float)

    model = relationship("TritonModels")
