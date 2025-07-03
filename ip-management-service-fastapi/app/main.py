from fastapi import FastAPI
from app.routes import router as ip_router
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.config import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()

app = FastAPI(
	title="IP Management Service",
	version="1.0.0"
)
app.include_router(ip_router)

# Split string into list of origins
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
