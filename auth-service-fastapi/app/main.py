# from fastapi import FastAPI
# from app.auth.routes import router as auth_router

# app = FastAPI()

# app.include_router(auth_router, prefix="/api")

# @app.get("/")
# async def read_root():
# 	return {"message": "Welcome to the JWT Auth Microservice!"}

from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI()

app.include_router(auth_router)  # No need for prefix again, it's already inside routes.py
