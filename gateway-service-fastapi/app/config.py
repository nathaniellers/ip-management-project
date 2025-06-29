from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
  auth_service_url: str
  ip_service_url: str

  class Config:
    env_file = ".env"

