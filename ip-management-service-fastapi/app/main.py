from fastapi import FastAPI
from app.routes import router as ip_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="IP Management Service")

app.include_router(ip_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the IP Management Service!"}
