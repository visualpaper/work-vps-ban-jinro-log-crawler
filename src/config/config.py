from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    logging_path: str = ""
    read_wait_seconds: float = 0
    read_count_limit: int = 0
    proxy: str = ""
    mongodb_url: str = ""
    mongodb_dbname: str = ""
    mongodb_min_connection_pool: int = 0
    mongodb_max_connection_pool: int = 0

    class Config:
        env_file = ".env"


@lru_cache()
def get_config() -> Settings:
    return Settings()
