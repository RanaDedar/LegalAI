from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

_PACKAGE_ROOT = Path(__file__).resolve().parents[1]
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_PACKAGE_ROOT / ".env"),
        extra="ignore",
    )
    DB_CONNECTION: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    EXP_TIME: int = 100

setting = Settings()

