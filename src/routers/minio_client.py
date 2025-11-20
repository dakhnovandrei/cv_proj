from minio import Minio
import os
from minio.error import S3Error
import io
import uuid

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_SECURE = bool(os.getenv("MINIO_SECURE"))
BUCKET_NAME = os.getenv("BUCKET_NAME")

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE
)


def ensure_bucket_exist(bucket_name: str = BUCKET_NAME):
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f'bucket create successfully, name: {bucket_name}')
    except S3Error as e:
        print(f'Error, Type: {e}')
        raise


def upload_images(file_data: bytes, filename: str, content_type: str = "image/jpeg") -> str:
    try:
        file_extension = filename.split('.')[-1] if '.' in filename else 'jpg'
        unique_filename = f'{uuid.uuid4()}.{file_extension}'

        file_like_obj = io.BytesIO(file_data)

        minio_client.put_object(
            BUCKET_NAME,
            unique_filename,
            file_like_obj,
            length=len(file_data),
            content_type=content_type,
        )

        return f'http://{MINIO_ENDPOINT}/{BUCKET_NAME}/{unique_filename}'

    except S3Error as e:
        print(f'Error, Type: {e}')
        raise


def delite_image(filename: str):
    try:
        minio_client.remove_object(BUCKET_NAME, filename)
    except S3Error as e:
        print(f'Error. Type: {e}')
        raise


def get_image_url(filename: str) -> str:
    return f'http://{MINIO_ENDPOINT}/{BUCKET_NAME}/{filename}'


ensure_bucket_exist()
