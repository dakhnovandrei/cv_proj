import os.path
import sys
import tempfile

import cv2
from fastapi import HTTPException, Depends, APIRouter, UploadFile, File
from fastapi.responses import Response
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import ProccessingRes

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ai_model.analysis import detection_with_minio

analyze_router = APIRouter()


@analyze_router.post("/analyze", tags=["Analyze"])
async def analysis(
        file: UploadFile = File(...),
        color_threshold: float = 0.3,
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail='File must be image')

    try:
        contents = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        try:
            res_image = detection_with_minio(
                image_path=temp_path,
                color_threshold=color_threshold
            )

            res_image_rgb = cv2.cvtColor(res_image, cv2.COLOR_BGR2RGB)

            success, encoded_image = cv2.imencode('.jpg', res_image_rgb)
            if not success:
                raise HTTPException(status_code=500, detail="Fail to encode image")

            image_bytes = encoded_image.tobytes()
            return Response(
                content=image_bytes,
                media_type="image/jpeg",
                headers={
                    "Content-Disposition": f"attachment; filename=detected_{file.filename}"
                }
            )
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
