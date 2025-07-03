from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import AuditLog
from app.schemas import AuditLogOut

def get_audit_logs(skip: int, limit: int, search: str, db: Session, user):
  if user["role"] != "admin":
    raise HTTPException(status_code=403, detail="Forbidden")

  query = db.query(AuditLog)
  if search:
    query = query.filter(
      AuditLog.details.ilike(f"%{search}%") |
      AuditLog.ip.ilike(f"%{search}%") |
      AuditLog.name.ilike(f"%{search}%")
    )
  query = query.order_by(AuditLog.timestamp.desc())
  total = query.count()
  logs = query.offset(skip).limit(limit).all()
  return {
    "total": total,
    "data": [AuditLogOut.model_validate(log).model_dump() for log in logs]
  }
