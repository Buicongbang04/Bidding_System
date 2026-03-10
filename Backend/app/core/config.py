from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    upload_dir: str = "uploads"
    max_file_size_mb: int = 20
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5:7b"
    ollama_timeout_seconds: int = 120

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
