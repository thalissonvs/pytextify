from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    BACKEND_URL: str = 'redis://localhost:6379/0'
    BROKER_URL: str = 'pyamqp://guest@localhost//'
