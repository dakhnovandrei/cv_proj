from datetime import timedelta
from urllib.parse import urlparse
from minio import Minio
import os
from minio.error import S3Error
import io
import uuid

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_PUBLIC_URL = os.getenv("MINIO_PUBLIC_URL")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_SECURE = bool(os.getenv("MINIO_SECURE"))
MINIO_PORT = os.getenv("MINIO_PORT")
BUCKET_NAME = os.getenv("BUCKET_NAME")

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)


def make_bucket_public(bucket_name: str):
    public_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetObject"],
                "Resource": ["arn:aws:s3:::plant-disease-image/*"]
            }
        ]
    }

    import json
    policy_str = json.dumps(public_policy)

    minio_client.set_bucket_policy(bucket_name, policy_str)


def ensure_bucket_exist(bucket_name: str = BUCKET_NAME):
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f'bucket create successfully, name: {bucket_name}')
            make_bucket_public(bucket_name)
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

        return f'http://{MINIO_PUBLIC_URL}/{BUCKET_NAME}/{unique_filename}'

    except S3Error as e:
        print(f'Error, Type: {e}')
        raise


def delete_image(filename: str):
    try:
        minio_client.remove_object(BUCKET_NAME, filename)
    except S3Error as e:
        print(f'Error. Type: {e}')
        raise


def get_private_image_url(filename: str, expires=3600) -> str:
    try:
        url = minio_client.presigned_get_object(
            BUCKET_NAME,
            filename,
            expires=timedelta(seconds=expires),
        )
        return url
    except S3Error as e:
        raise


ensure_bucket_exist()
