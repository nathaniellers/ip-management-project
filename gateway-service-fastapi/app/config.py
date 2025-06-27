from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
  auth_service_url: str
  ip_service_url: str

  class Config:
    env_file = ".env"
