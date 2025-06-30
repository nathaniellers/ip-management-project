from fastapi import APIRouter, Request, Header
from app.config import Settings

import httpx

router = APIRouter()
settings = Settings()

@router.post("/login")
async def proxy_login(request: Request):
	body = await request.json()
	async with httpx.AsyncClient() as client:
		response = await client.post(f"{settings.AUTH_SERVICE_URL}/api/login", json=body)
		return response.json()

@router.post("/logout")
async def proxy_logout(request: Request, authorization: str = Header(...)):
	async with httpx.AsyncClient() as client:
		response = await client.post(
				f"{settings.AUTH_SERVICE_URL}/api/logout",
				headers={"Authorization": authorization}
		)
		return response.json()
	
@router.post("/register")
async def proxy_register(request: Request):
	body = await request.json()
	async with httpx.AsyncClient() as client:
		response = await client.post(f"{settings.AUTH_SERVICE_URL}/api/register", json=body)
		return response.json()
	
@router.get("/ip")
async def get_ip():
	async with httpx.AsyncClient() as client:
		response = await client.get(f"{settings.IP_SERVICE_URL}/ip")
	return response.json()

@router.post("/ip")
async def create_ip():
	async with httpx.AsyncClient() as client:
		response = await client.get(f"{settings.IP_SERVICE_URL}/ip")
	return response.json()
