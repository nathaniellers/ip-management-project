from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.models import AuditLog
from app.schemas import AuditLogCreate, ActionType, ResourceType

def create_audit_log_entry(log: AuditLogCreate, db: Session):
  db_log = AuditLog(**log.dict())
  db.add(db_log)
  db.commit()

def get_filtered_audit_logs(
  db: Session,
  search: str = None,
  action: str = None,
  resource: str = None,
  session_id: str = None,
  ip: str = None,
  start_date: str = None,
  end_date: str = None,
  page: int = 0,
  limit: int = 10
):
  query = db.query(AuditLog)

  if search:
    like = f"%{search}%"
    query = query.filter(
      or_(
        AuditLog.name.ilike(like),
        AuditLog.session_id.ilike(like),
        AuditLog.ip.ilike(like),
        AuditLog.details.ilike(like)
      )
    )

  if action:
    try:
      query = query.filter(AuditLog.action == ActionType(action))
    except ValueError:
      raise HTTPException(status_code=400, detail=f"Invalid action: {action}")

  if resource:
    try:
      query = query.filter(AuditLog.resource == ResourceType(resource))
    except ValueError:
      raise HTTPException(status_code=400, detail=f"Invalid resource: {resource}")

  if session_id:
    query = query.filter(AuditLog.session_id == session_id)
  if ip:
    query = query.filter(AuditLog.ip == ip)

  if start_date:
    try:
      start = datetime.strptime(start_date, "%Y-%m-%d")
      query = query.filter(AuditLog.timestamp >= start)
    except ValueError:
      raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD")

  if end_date:
    try:
      end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
      query = query.filter(AuditLog.timestamp < end)
    except ValueError:
      raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD")

  total = query.count()

  logs = (
    query.order_by(AuditLog.timestamp.desc())
    .offset(page * limit)
    .limit(limit)
    .all()
  )

  return {
    "total": total,
    "logs": [
      {
        "id": str(log.id),
        "actor_id": str(log.actor_id),
        "session_id": str(log.session_id),
        "name": log.name,
        "ip": log.ip,
        "action": log.action.value,
        "resource": log.resource.value,
        "details": log.details,
        "timestamp": log.timestamp.isoformat() if log.timestamp else None
      }
      for log in logs
    ]
  }
