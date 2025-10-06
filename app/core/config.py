from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Omni Synesis"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 5050
    API_PREFIX: str = "x"

    # Model
    MODEL_CHECKPOINT: str = "yainage90/fashion-object-detection"
    DETECTION_THRESHOLD: float = 0.4

    # Security
    SECRET_KEY: str = "xxx"
    ALGORITHM: str = ".xxx"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()