
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DB_HOST:str
    DB_PORT:int
    DB_USER:str
    DB_PASSWORD:str
    DB_NAME:str
    DB_URL:str
    SECRET_KEY:str
    ALGORITHM:str  
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    SERVER_HOST:str
    SERVER_PORT:int
    ENVIRONMENT:str
    DEBUG:bool
    ALLOWED_TYPES:list[str] = ["image/jpeg", "image/png"]
    MAX_FILE_SIZE:int = 2 * 1024 * 1024  # 2 MB
    class Config:
        env_file = ".env"
settings = Settings()
