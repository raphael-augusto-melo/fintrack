from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "development"
    DATABASE_URL: str
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    JWT_SECRET: str = "dev-secret-change-me"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [origin.strip() for origin in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

def get_settings() -> Settings:
    return Settings()

settings = get_settings()