from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "BTG Funds API"
    MONGO_URI: str
    DATABASE_NAME: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
