import logging
import os
from src.models import Users, UserRequests, AnalysisResult, Diseases
from src.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from datetime import timedelta
from sqlalchemy.orm import Session
from src.routers.auth import create_access_token, create_refresh_token, pwd_context, get_current_user
from dotenv import load_dotenv
from src.schemas import UserCreate, AuthResponse, UserLogin, AnalysisHistoryList, DiseaseResult, AnalysisHistoryItem

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()

logger = logging.getLogger("uvicorn")  # использовать логгер Uvicorn
logger.setLevel(logging.INFO)


@router.post("/reg", tags=["Auth"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    exist_user = db.query(Users).filter(Users.email == user.email).first()

    if exist_user:
        raise HTTPException(status_code=401, detail="Пользователь уже зарегистрирован")
    hashed_password = pwd_context.hash(user.password)
    print(hashed_password)
    new_user = Users(
        email=user.email,
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "User_id": new_user.user_id}


@router.post("/login", summary="login in account", tags=["Auth"])
def login(users: UserLogin, response: Response, db: Session = Depends(get_db)) -> AuthResponse:
    user = db.query(Users).filter(Users.email == users.email).first()
    logger.info(user)
    if not user or not pwd_context.verify(users.password, user.password):
        raise HTTPException(status_code=401, detail="Неправильная почта или пароль")

    access_token = create_access_token(
        data={'sub': user.email, },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    refresh_token = create_refresh_token(
        data={'sub': user.email, },
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        samesite="lax",
    )

    return AuthResponse(access_token=access_token, refresh_token=refresh_token)


@router.get('/analysis_history', tags=["History"], response_model=AnalysisHistoryList)
def request_history(
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(10, ge=1, le=100, description="Items per page"),
        current_user: Users = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    try:
        offset = (page - 1) * page_size
        user_requests = db.query(UserRequests).filter(UserRequests.user_id == current_user.user_id).order_by(
            UserRequests.timestamp.desc()).offset(offset).limit(page_size).all()
        total = db.query(UserRequests).filter(UserRequests.user_id == current_user.user_id).count()

        history_items = []

        for request in user_requests:
            analysis_res = db.query(AnalysisResult).filter(AnalysisResult.request_id == request.request_id).all()
            disease_res = []
            for res in analysis_res:
                disease = db.query(Diseases).filter(Diseases.disease_id == res.disease_id).first()

                if disease:
                    disease_res.append(
                        DiseaseResult(
                            disease=disease.disease_name,
                            recommendation=disease.recommendation
                        )
                    )
            history_item = AnalysisHistoryItem(
                request_id=request.request_id,
                image_url=request.image_path,
                created_at=request.timestamp,
                results=disease_res
            )
            history_items.append(history_item)

        return AnalysisHistoryList(
            total=total,
            page=page,
            page_size=page_size,
            history=history_items
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении истории {e}")


@router.get("/analysis_history/{request_id}", response_model=AnalysisHistoryItem, tags=["History"])
def request_analysis(
        request_id: int,
        user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user_request = db.query(UserRequests).filter(UserRequests.request_id == request_id,
                                                 UserRequests.user_id == user.user_id).first()

    if not user_request:
        raise HTTPException(status_code=404, detail=f"Анализ не найден или у вас нет доступа")

    analysis_res = db.query(AnalysisResult).filter(AnalysisResult.request_id == request_id).all()

    disease_res = []
    for res in analysis_res:
        disease = db.query(Diseases).filter(Diseases.disease_id == res.disease_id).first()
        if disease:
            disease_res.append(
                DiseaseResult(
                    disease=disease.disease_name,
                    recommendation=disease.recommendation
                ))
    return AnalysisHistoryItem(
        request_id=user_request.request_id,
        image_url=user_request.image_path,
        created_at=user_request.timestamp,
        results=disease_res
    )
