from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str = "mysql+aiomysql://dev:dev@localhost:3306/engineer_support"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    LLM_API_KEY: str = ""
    LLM_API_BASE: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    MAX_UPLOAD_SIZE_MB: int = 50
    ATTACHMENT_STORAGE_PATH: str = "./storage/attachments"


settings = Settings()
