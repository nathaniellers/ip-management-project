from fastapi import FastAPI
from app.routes import router as audit_router
from app.config import Settings
from fastapi.middleware.cors import CORSMiddleware

settings = Settings()

app = FastAPI(
	title="Audit Service",
	version="1.0.0"
)

app.include_router(audit_router)

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