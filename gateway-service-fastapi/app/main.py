# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.config import Settings
from app.routes import router

settings = Settings()

app = FastAPI(
    title="JWT Gateway Service",
    version="1.0.0"
)

# Split string into list of origins
origins = settings.ALLOWED_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the JWT Gateway Service!"}
