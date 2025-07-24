# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:int
    DB_NAME:str
    DATABASE_URL: str
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS:int
    
    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int
    
    GOOGLE_CLIENT_ID:str
    GOOGLE_CLIENT_SECRET:str
    
    class Config:
        env_file = ".env"

settings = Settings()
