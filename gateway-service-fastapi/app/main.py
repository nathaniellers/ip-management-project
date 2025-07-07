from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import Settings
from app.routes import router
from app.queue.audit_worker import audit_worker

settings = Settings()

app = FastAPI(
	title="JWT Gateway Service",
	version="1.0.0"
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.ALLOWED_ORIGINS,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup():
	import asyncio
	asyncio.create_task(audit_worker())

@app.get("/")
async def read_root():
	return {"message": "Welcome to the JWT Gateway Service!"}
