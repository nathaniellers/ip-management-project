from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DATABASE_URL: str
  ALLOWED_ORIGINS: str
  SECRET_KEY: str
  INTERNAL_KEY: str
  ALGORITHM: str

  class Config:
    env_file = ".env"
