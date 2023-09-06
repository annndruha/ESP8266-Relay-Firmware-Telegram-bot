from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    BOT_TOKEN: str
    RELAY_URL: str

    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="allow")
