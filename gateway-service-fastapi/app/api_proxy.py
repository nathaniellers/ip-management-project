import httpx
import os

AUTH_URL = os.getenv("AUTH_SERVICE_URL")
IP_URL = os.getenv("IP_SERVICE_URL")
AUDIT_URL = os.getenv("AUDIT_SERVICE_URL")

async def forward_request(service_url: str, path: str, method: str = "GET", headers=None, json=None, params=None):
	async with httpx.AsyncClient() as client:
		response = await client.request(
			method=method,
			url=f"{service_url}{path}",
			headers=headers,
			json=json,
			params=params
		)
		return response
