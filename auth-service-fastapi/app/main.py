from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import router as auth_router
from app.queue.audit_worker import audit_worker
from contextlib import asynccontextmanager
from app.config import Settings
import asyncio
import logging

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
	task = asyncio.create_task(audit_worker())	
	yield 
	task.cancel()

	try:
		await task
	except asyncio.CancelledError:
		pass

app = FastAPI(
	title="Auth Service",
	version="1.0.0",
	lifespan=lifespan
)

app.include_router(auth_router, prefix="/api")

app.add_middleware(
	CORSMiddleware,
	allow_origins=[settings.ALLOWED_ORIGINS],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/")
async def read_root():
	return {"message": "Welcome to the Auth Microservice!"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

