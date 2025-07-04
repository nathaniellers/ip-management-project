from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies import verify_internal_key
from app.database import get_db
from app.schemas import AuditLogCreate
from app.services import create_audit_log_entry, get_filtered_audit_logs
from app.config import Settings

router = APIRouter(prefix="/api", tags=["Audit Management"])
settings = Settings()

@router.post("/logs", status_code=status.HTTP_201_CREATED)
def create_log(
  log: AuditLogCreate,
  db: Session = Depends(get_db),
  _ = Depends(verify_internal_key)
):
  create_audit_log_entry(log, db)
  return {"message": "Audit log created"}

@router.get("/logs")
def get_logs(
  db: Session = Depends(get_db),
  search: Optional[str] = Query(None),
  action: Optional[str] = None,
  resource: Optional[str] = None,
  session_id: Optional[str] = None,
  ip: Optional[str] = None,
  start_date: Optional[str] = None,
  end_date: Optional[str] = None,
  page: int = 0,
  limit: int = 10,
):
  return get_filtered_audit_logs(
    db=db,
    search=search,
    action=action,
    resource=resource,
    session_id=session_id,
    ip=ip,
    start_date=start_date,
    end_date=end_date,
    page=page,
    limit=limit
  )
