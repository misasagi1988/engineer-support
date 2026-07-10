from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str = "mysql+aiomysql://dev:dev@localhost:3306/engineer_support"
    SECRET_KEY: str | None = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    LLM_API_KEY: str = ""
    LLM_API_BASE: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    MAX_UPLOAD_SIZE_MB: int = 50
    ATTACHMENT_STORAGE_PATH: str = "./storage/attachments"
    CORS_ORIGINS: str = "*"  # comma-separated list or "*" for dev

    @model_validator(mode="after")
    def check_secret_key(self) -> "Settings":
        if not self.SECRET_KEY or self.SECRET_KEY in ("change-me-in-production", "dev-secret-key"):
            raise ValueError(
                "SECRET_KEY must be set to a strong random value in production. "
                "Set it via environment variable or .env file."
            )
        return self

    @property
    def cors_origins_list(self) -> list[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
