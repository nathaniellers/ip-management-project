from fastapi import APIRouter, Request
import httpx

router = APIRouter()

AUTH_SERVICE_URL = "http://localhost:8001/api"
IP_SERVICE_URL = "http://localhost:8002/api"

@router.post("/login")
async def login(request: Request):
	data = await request.json()
	async with httpx.AsyncClient() as client:
		response = await client.post(f"{AUTH_SERVICE_URL}/login", json=data)
	return response.json()

@router.get("/ips")
async def get_ips():
	async with httpx.AsyncClient() as client:
			response = await client.get(f"{IP_SERVICE_URL}/ips")
	return response.json()
