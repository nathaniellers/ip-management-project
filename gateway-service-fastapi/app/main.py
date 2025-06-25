# from fastapi import FastAPI
# from app.routes import router

# app = FastAPI(title="Gateway Service")
# app.include_router(router, prefix="/api")

# @app.get("/")
# async def read_root():
# 	return {"message": "Welcome to the JWT Gateway Microservice!"}

from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.post("/api/login")
async def proxy_login(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://auth-service:8001/api/login", json=body)
        return response.json()
