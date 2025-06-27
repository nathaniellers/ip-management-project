from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.models import Base
from app.database.db import engine
from app.auth.routes import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
  Base.metadata.create_all(bind=engine)
  yield
  
app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/api")

@app.get("/")
async def read_root():
	return {"message": "Welcome to the JWT Auth Microservice!"}

