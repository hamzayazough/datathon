import os
from dotenv import load_dotenv

load_dotenv()

AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
