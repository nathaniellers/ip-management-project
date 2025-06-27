from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	DATABASE_URL: str
	SECRET_KEY: str
	ALGORITHM: str
	ACCESS_TOKEN_EXPIRE_MINUTES: int
	REFRESH_TOKEN_EXPIRE_DAYS: int
	REDIS_URL: str
	AUTH_SERVICE_URL: str

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		populate_by_name=True
	)

settings = Settings()

