from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  AUTH_SERVICE_URL: str
  IP_SERVICE_URL: str
  ALLOWED_ORIGINS: str
  SECRET_KEY: str
  AUDIT_SERVICE_URL: str
  INTERNAL_KEY: str
  ALGORITHM: str

  class Config:
    env_file = ".env"

