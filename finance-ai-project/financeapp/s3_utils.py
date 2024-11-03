import os
import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, S3_BUCKET_NAME

s3_client = boto3.client(
    's3',
    region_name=os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

def upload_to_s3(file_path, s3_key):
    s3_client.upload_file(file_path, S3_BUCKET_NAME, s3_key)
    print(f"Fichier {file_path} envoyé à S3 avec la clé {s3_key}")

def download_from_s3(s3_key, local_path):
    s3_client.download_file(S3_BUCKET_NAME, s3_key, local_path)
    print(f"Fichier {s3_key} téléchargé depuis S3 vers {local_path}")
