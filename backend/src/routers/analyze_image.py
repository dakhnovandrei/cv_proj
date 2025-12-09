import os.path
import sys
import tempfile
from ..schemas import AnalysisResponse
from fastapi import HTTPException, Depends, APIRouter, UploadFile, File
from .auth import get_current_user
from ..database import get_db
from sqlalchemy.orm import Session
from ai_model.analysis import detection_with_minio 
from ..models import AnalysisResult, Diseases, UserRequests
from sqlalchemy import func

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

analyze_router = APIRouter()


@analyze_router.post("/analyze", tags=["Analyze"], response_model=AnalysisResponse)
async def analysis(
        file: UploadFile = File(...),
        user=Depends(get_current_user),
        color_threshold: float = 0.3,
        db: Session = Depends(get_db)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail='File must be image')

    contents = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        res_image_url, color_stats = detection_with_minio(
            image_path=temp_path,
            color_threshold=color_threshold
        )
        print(color_stats)
        if not res_image_url:
            raise HTTPException(status_code=500, detail="Ошибка в загрузке изображения в MinIO")
        user_request = UserRequests(
            user_id=user.user_id,
            image_path=res_image_url
        )
        db.add(user_request)
        db.commit()
        db.refresh(user_request)

        results = []

        for info in color_stats:
            disease_name = info["class"]
            confidence = float(info["confidence"])

            disease = db.query(Diseases).filter(func.lower(Diseases.disease_name) == disease_name.lower()).first()
            if not disease:
                print(f"[DEBUG] Disease not found in DB: '{disease_name}'")
                continue

            analysis_res = AnalysisResult(
                request_id=user_request.request_id,
                disease_id=disease.disease_id,
                processed_image=res_image_url,
                confidence=confidence,
            )
            db.add(analysis_res)
            results.append({
                "disease": disease.disease_name,
                "confidence": round(confidence, 2),
                "recommendation": disease.recommendation
            })
        db.commit()

        return AnalysisResponse(
            image_url=res_image_url,
            results=results
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
