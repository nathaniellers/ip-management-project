from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import AuditLog
from app.schemas import AuditLogCreate
from datetime import datetime
from app.dependencies import get_current_user
from app.services import get_audit_logs
import pytz

router = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
      db.close()

@router.post("/audit-log", status_code=201)
def create_log(
    log: AuditLogCreate,
    db: Session = Depends(get_db)
  ):
  
  ph_timezone = pytz.timezone("Asia/Manila")
  now_ph = datetime.now(ph_timezone)

  log_entry = AuditLog(
    actor_id=log.actor_id,
    name=log.name,
    action=log.action,
    ip=log.ip,
    ip_id=log.ip_id,
    details=log.details,
    timestamp=now_ph
  )
  db.add(log_entry)
  db.commit()
  return {"message": "Audit log created"}

@router.get("/logs")
def get_audit_log(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
  ):
    
	return get_audit_logs(
    skip,
    limit,
    search,
    db,
    user
  )
