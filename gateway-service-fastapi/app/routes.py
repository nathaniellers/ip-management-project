from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from app.config import Settings
from app.schema import IPCreate
from app.dependencies import get_current_user
from uuid import UUID
import logging
import httpx
from typing import Optional

router = APIRouter()
settings = Settings()
logger = logging.getLogger(__name__)

@router.post("/login")
async def proxy_login(request: Request):
	try:
		body = await request.json()
		async with httpx.AsyncClient() as client:
			response = await client.post(
				f"{settings.AUTH_SERVICE_URL}/api/login",
				json=body,
				headers={"Content-Type": "application/json"},
			)

		if response.status_code != 200:
			raise HTTPException(status_code=response.status_code, detail=response.text)

		# Forward the response body
		result = response.json()
		proxy_response = JSONResponse(content=result, status_code=response.status_code)

		# ✅ Forward the refresh_token cookie from auth service
		if "set-cookie" in response.headers:
			proxy_response.headers["set-cookie"] = response.headers["set-cookie"]

		return proxy_response

	except Exception as e:
		raise HTTPException(status_code=500, detail="Unexpected error")

@router.post("/logout")
async def proxy_logout(authorization: str = Header(...)):
	try:
		async with httpx.AsyncClient() as client:
			response = await client.post(
					f"{settings.AUTH_SERVICE_URL}/api/logout",
					headers={"Authorization": authorization}
			)
			return response.json()
	except Exception as e:
		logger.error(f"Unexpected error: {str(e)}")
		raise HTTPException(status_code=500, detail="Internal gateway error")
	
@router.post("/register")
async def proxy_register(request: Request):
	try:
		body = await request.json()
		async with httpx.AsyncClient() as client:
			response = await client.post(f"{settings.AUTH_SERVICE_URL}/api/register", json=body)
			return response.json()
	except Exception as e:
		logger.error(f"Unexpected error: {str(e)}")
		raise HTTPException(status_code=500, detail="Internal gateway error")

from fastapi.responses import JSONResponse

@router.post("/refresh")
async def proxy_refresh_token(request: Request):
	try:
		refresh_token = request.cookies.get("refresh_token")
		logger.info(f"Refresh token from cookies: {refresh_token}")
		if not refresh_token:
			raise HTTPException(status_code=401, detail="Missing refresh token")

		async with httpx.AsyncClient() as client:
			response = await client.post(
				f"{settings.AUTH_SERVICE_URL}/api/refresh",
				json={"refresh_token": refresh_token},  # ✅ Fix: Send the body expected
				headers={"Content-Type": "application/json"},
				cookies=request.cookies
			)

			logger.info(f"Response: {response}")

		if response.status_code != 200:
			logger.error(f"Failed to refresh token: {response.text}")
			raise HTTPException(
				status_code=response.status_code,
				detail=response.json().get("detail", "Refresh failed")
			)

		# Forward access_token and set-cookie header
		result = response.json()
		proxy_response = JSONResponse(content=result, status_code=response.status_code)

		if "set-cookie" in response.headers:
			proxy_response.headers["set-cookie"] = response.headers["set-cookie"]

		return proxy_response

	except Exception as e:
		logger.exception("Unexpected error in token refresh proxy")
		raise HTTPException(status_code=500, detail="Unexpected error")


@router.get("/ip/")
async def get_ip(
	authorization: str = Header(...),
	page: int = Query(1, ge=1),
	limit: int = Query(10, ge=1, le=100),
	search: str = Query(None),
	user=Depends(get_current_user)
):
	skip = (page - 1) * limit 

	params = {
		"skip": skip,
		"limit": limit
	}

	if search:
		params["search"] = search

	async with httpx.AsyncClient() as client:
		try:
			response = await client.get(
				f"{settings.IP_SERVICE_URL}/api/ip/",
				headers={"Authorization": authorization},
				params=params
			)
			response.raise_for_status()
			return response.json()
		except Exception as e:
			logger.error(f"Unexpected error during GET /ip/: {str(e)}")
			raise HTTPException(status_code=500, detail="Internal gateway error")

@router.post("/ip/")
async def create_ip(
	payload: IPCreate,
	authorization: str = Header(...),
	user=Depends(get_current_user)
):
	async with httpx.AsyncClient() as client:
		try:
			response = await client.post(
				f"{settings.IP_SERVICE_URL}/api/ip/",
				headers={"Authorization": authorization},
				json=payload.dict()
			)
			response.raise_for_status()
			return response.json()
		except Exception as e:
			logger.error(f"Unexpected error during POST /ip/: {str(e)}")
			raise HTTPException(status_code=500, detail="Internal gateway error")

@router.put("/ip/{ip_id}")
async def proxy_update_ip(
	ip_id: UUID,
	payload: dict,
	authorization: str = Header(...),
	user=Depends(get_current_user)
):
	try:
		async with httpx.AsyncClient() as client:
			response = await client.put(
				f"{settings.IP_SERVICE_URL}/api/ip/{ip_id}",
				headers={"Authorization": authorization},
				json=payload
			)
			response.raise_for_status()
			return response.json()
	except Exception as e:
		logger.error(f"Unexpected error during PUT /ip/{ip_id}: {str(e)}")
		raise HTTPException(status_code=500, detail="Internal gateway error")

@router.delete("/{ip_id}", status_code=204)
async def proxy_delete_ip(
	ip_id: UUID,
	request: Request,
	user=Depends(get_current_user)
):
	try:
		async with httpx.AsyncClient() as client:
			response = await client.delete(
				f"{settings.IP_SERVICE_URL}/api/ip/{ip_id}",
				headers={"Authorization": request.headers.get("Authorization")}
			)

			if response.status_code != 204:
				raise HTTPException(
					status_code=response.status_code,
					detail=response.text
				)

	except httpx.RequestError as e:
		raise HTTPException(
			status_code=502,
			detail=f"IP service unreachable: {str(e)}"
		)

@router.get("/logs")
async def proxy_get_logs(
    authorization: str = Header(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    action: Optional[str] = None,
    resource: Optional[str] = None,
    session_id: Optional[str] = None,
    ip: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    user=Depends(get_current_user)
):
    skip = (page - 1) * limit

    params = {
        "page": page - 1,
        "limit": limit,
    }

    if search:
        params["search"] = search
    if action:
        params["action"] = action
    if resource:
        params["resource"] = resource
    if session_id:
        params["session_id"] = session_id
    if ip:
        params["ip"] = ip
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.AUDIT_SERVICE_URL}/api/logs",
                headers={"Authorization": authorization},
                params=params
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Audit Service: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            logger.error(f"Unexpected error during audit log proxy call: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal gateway error")
