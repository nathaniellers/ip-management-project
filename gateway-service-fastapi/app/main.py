from fastapi import FastAPI, Request
from app.config import Settings
from app.routes import router

app = FastAPI()
settings = Settings()
app.include_router(router, prefix="/api")

@app.get("/")
async def read_root():
	print(f"route {settings.IP_SERVICE_URL}")
	return {"message": "Welcome to the JWT Gateway Service!"}
