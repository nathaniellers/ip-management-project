from fastapi import FastAPI
from app.routes import router as ip_router
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.config import Settings
from app.queue.audit_worker import audit_worker
from contextlib import asynccontextmanager
import asyncio

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
	title="IP Management Service",
	version="1.0.0",
	lifespan=lifespan
)
app.include_router(ip_router)

origins = settings.ALLOWED_ORIGINS.split(",")

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/")
async def read_root():
	return {"message": "Welcome to the IP Management Service!"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
