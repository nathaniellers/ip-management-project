from fastapi import FastAPI
from app.schema import LoginRequest, LogoutRequest, RegisterRequest
from app.config import Settings
import httpx

app = FastAPI()
settings = Settings()

@app.get("/")
async def read_root():
	return {"message": "Welcome to the JWT Gateway Service!"}

@app.post("/api/login")
async def proxy_login(request: LoginRequest):
	body = await request.json()
	async with httpx.AsyncClient() as client:
		response = await client.post(f"{settings.auth_service_url}/api/login", json=body)
		return response.json()

@app.post("/api/logout")
async def proxy_logout(request: LogoutRequest):
	body = await request.json()
	async with httpx.AsyncClient() as client:
		response = await client.post(f"{settings.auth_service_url}/api/logout", json=body)
		return response.json()
	
@app.post("/api/register")
async def proxy_register(request: RegisterRequest):
	body = await request.json()
	async with httpx.AsyncClient() as client:
		response = await client.post(f"{settings.auth_service_url}/api/register", json=body)
		return response.json()
