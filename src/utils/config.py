from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    # UPLODED_FILES_PATH: str
    FILE_DEFAULT_MAX_CHUNK_SIZE: int

    LOGGING_PATH: str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()
