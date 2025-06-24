from fastapi import FastAPI
from app.auth import routes as auth_routes

app = FastAPI(
	title="JWT Auth Microservice",
	description="A simple FastAPI microservice for user authentication using JWT.",
	version="1.0.0",
)

app.include_router(auth_routes.router)

@app.get("/")
async def read_root():
	return {"message": "Welcome to the JWT Auth Microservice!"}

