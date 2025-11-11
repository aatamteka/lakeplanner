from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://lakeuser:lakepass@localhost:5432/lakeplatform"
    RABBITMQ_URL: str = "amqp://admin:admin@localhost:5672/"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
