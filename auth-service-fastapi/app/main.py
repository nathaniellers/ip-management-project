from fastapi import FastAPI

from app.auth.routes import router as auth_router

app = FastAPI(title="Auth Service")

app.include_router(auth_router, prefix="/api")

@app.get("/")
async def read_root():
	return {"message": "Welcome to the JWT Auth Microservice!"}

