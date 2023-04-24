from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    BOT_TOKEN: str
    RELAY_URL: str

    class Config:
        """Pydantic BaseSettings config"""
        case_sensitive = True
        env_file = ".env"
