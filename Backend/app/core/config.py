from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    upload_dir: str = "uploads"
    max_file_size_mb: int = 20

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()