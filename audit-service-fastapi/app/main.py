from fastapi import FastAPI
from app.routes import router as audit_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Audit Log Service")

app.include_router(audit_router)
