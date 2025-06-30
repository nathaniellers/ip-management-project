from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
  AUTH_SERVICE_URL: str
  IP_SERVICE_URL: str

  class Config:
    env_file = ".env"

