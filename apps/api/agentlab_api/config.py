from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    agentlab_env: str = "development"
    database_url: str = "sqlite+aiosqlite:///./agentlab.db"
    openai_base_url: str = "mock://agentlab"
    openai_api_key: str = ""
    agentlab_secret_redaction: bool = True
    agentlab_default_policy: str = "ask"


@lru_cache
def get_settings() -> Settings:
    return Settings()

