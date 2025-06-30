from app.models import IPAddress, AuditLog
from app.database import SessionLocal
from app.schemas import IPCreate, IPUpdate
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Create IP (admin and regular users)
async def create_ip(ip_data: IPCreate, user_id: UUID):
    db: Session = next(get_db())
    new_ip = IPAddress(**ip_data.dict(), created_by=user_id)
    db.add(new_ip)
    db.commit()
    db.refresh(new_ip)

    log = AuditLog(
        user_id=user_id,
        ip_id=new_ip.id,
        action="CREATE",
        details=f"Created IP: {ip_data.ip}"
    )
    db.add(log)
    db.commit()
    return new_ip

# 2, 3, 4. Update IP (label only), enforce ownership or admin
async def update_ip(ip_id: UUID, update_data: IPUpdate, user_id: UUID, is_superuser: bool):
    db: Session = next(get_db())
    ip_record = db.query(IPAddress).filter(IPAddress.id == ip_id).first()

    if not ip_record:
        raise HTTPException(status_code=404, detail="IP address not found")

    if not is_superuser and ip_record.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this IP")

    ip_record.label = update_data.label
    db.commit()
    db.refresh(ip_record)

    log = AuditLog(
        user_id=user_id,
        ip_id=ip_id,
        action="UPDATE",
        details=f"Updated label to '{update_data.label}'"
    )
    db.add(log)
    db.commit()
    return ip_record

# 4. Delete IP (only for super-admins)
async def delete_ip(ip_id: UUID, user_id: UUID, is_superuser: bool):
    if not is_superuser:
        raise HTTPException(status_code=403, detail="Only super-admins can delete IPs")

    db: Session = next(get_db())
    ip_record = db.query(IPAddress).filter(IPAddress.id == ip_id).first()

    if not ip_record:
        raise HTTPException(status_code=404, detail="IP address not found")

    db.delete(ip_record)

    log = AuditLog(
        user_id=user_id,
        ip_id=ip_id,
        action="DELETE",
        details=f"Deleted IP: {ip_record.ip}"
    )
    db.add(log)
    db.commit()

    return {"message": "IP deleted"}

# 5. View all IPs (any user)
async def get_all_ips():
    db: Session = next(get_db())
    return db.query(IPAddress).all()

