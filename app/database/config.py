import os
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DB Migration API"
    DEBUG: bool = True
    
    # Database Settings
    DB_TYPE: str = os.getenv("DB_TYPE", "postgresql")  # or "oracle"
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")  # 5432 for PostgreSQL, 1521 for Oracle
    DB_NAME: str = os.getenv("DB_NAME", "migration_db")  # For PostgreSQL
    DB_SID: str = os.getenv("DB_SID", "ORCL")  # For Oracle
    DB_ECHO_SQL: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    # CSV Settings
    CSV_DELIMITER: str = ","
    CSV_INPUT_DIR: Path = PROJECT_ROOT / "data/input"
    CSV_PROCESSED_DIR: Path = PROJECT_ROOT / "data/processed"
    
    # Batch Settings
    MAX_BATCH_SIZE: int = 1000
    
    # Security Settings
   # API_KEY: Optional[str] = os.getenv("API_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create data directories if they don't exist
settings.CSV_INPUT_DIR.mkdir(parents=True, exist_ok=True)
settings.CSV_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
