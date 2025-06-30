from sqlalchemy.orm import Session
from datetime import datetime
from app.models import AuditLog

def log_action(db: Session, user_id: str, ip_id: str, action: str, details: str):
  audit = AuditLog(
      actor_id=user_id,
      ip_id=ip_id,
      action=action,
      details=details,
      timestamp=datetime.utcnow()
  )
  db.add(audit)
  db.commit()
