from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LocalReach"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/localreach"
    SECRET_KEY: str = "supersecretkey"  # in production, read from env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True

settings = Settings()