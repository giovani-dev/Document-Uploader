import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    mongo_password = os.getenv('MONGO_PASSWORD')
    mongo_user = os.getenv('MONGO_USER')
    mongo_host = os.getenv('MONGO_HOST')
    auth_api_port =  int(os.getenv('AUTH_API_PORT'))
    jwt_token_secret = os.getenv('JWT_TOKEN_SECRET')
    jwt_token_expire_limit = int(os.getenv('JWT_TOKEN_EXPIRE_LIMIT'))
    jwt_refresh_token_expire_limit = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRE_LIMIT'))
    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_KEY')
    aws_region_name = os.getenv('AWS_REGION_NAME')
    aws_s3_bucket = os.getenv('AWS_S3_BUCKET')
    env = os.getenv('ENV')
