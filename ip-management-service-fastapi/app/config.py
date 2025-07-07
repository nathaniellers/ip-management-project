from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DATABASE_URL: str
  SECRET_KEY: str
  ALGORITHM: str
  AUTH_SERVICE_URL: str
  IP_SERVICE_URL: str
  REDIS_URL: str
  ALLOWED_ORIGINS: str
  TIMEZONE: str
  AUDIT_SERVICE_URL: str
  INTERNAL_KEY: str

  class Config:
    env_file = ".env"

settings = Settings()
