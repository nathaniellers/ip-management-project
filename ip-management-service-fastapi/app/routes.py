from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
import logging

from app.database import get_db
from app.models import IPAddress, AuditLog
from app.schemas import IPCreate, IPUpdate, IPOut
from app.dependencies import get_current_user
from app.audit_log import log_action

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/ip", tags=["IP Management"])


# ✅ Create IP - admin only
@router.post("/", response_model=IPOut, status_code=201)
def create_ip(data: IPCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    print("User Data", user)
    print("User role", user['role'])
    logger.info(f"User {user['id']} attempting to create IP")

    if user["role"] != "admin":
        logger.warning(f"Unauthorized IP creation attempt by user {user['id']}")
        raise HTTPException(status_code=403, detail="Only admins can add IP addresses")

    new_ip = IPAddress(
        ip=data.ip,
        label=data.label,
        comment=data.comment,
        created_by=user["id"],
        updated_at=datetime.utcnow()
    )
    db.add(new_ip)
    db.commit()
    db.refresh(new_ip)

    log_action(db, action="create", user_id=user["id"], ip_id=new_ip.id, details="Created IP")
    logger.info(f"IP {new_ip.id} created by user {user['id']}")

    return new_ip


# ✅ Update IP - Only admin or Owner
@router.put("/{ip_id}", response_model=IPOut)
def update_ip(ip_id: UUID, data: IPUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ip = db.query(IPAddress).filter(IPAddress.id == ip_id, IPAddress.deleted == False).first()

    if not ip:
        logger.warning(f"IP {ip_id} not found for update")
        raise HTTPException(status_code=404, detail="IP address not found")

    if user["role"] != "admin" and ip.created_by != user["id"]:
        logger.warning(f"Unauthorized update attempt by user {user['id']} on IP {ip_id}")
        raise HTTPException(status_code=403, detail="Not authorized to update this IP")

    ip.label = data.label
    ip.comment = data.comment
    ip.updated_at = datetime.utcnow()
    db.commit()

    log_action(db, action="update", user_id=user["id"], ip_id=ip.id, details="Updated label/comment")
    logger.info(f"IP {ip_id} updated by user {user['id']}")

    return ip


# ✅ Delete IP - admin only
@router.delete("/{ip_id}", status_code=204)
def delete_ip(ip_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["role"] != "admin":
        logger.warning(f"Unauthorized delete attempt by user {user['id']}")
        raise HTTPException(status_code=403, detail="Only admins can delete IPs")

    ip = db.query(IPAddress).filter(IPAddress.id == ip_id, IPAddress.deleted == False).first()

    if not ip:
        logger.warning(f"IP {ip_id} not found for deletion")
        raise HTTPException(status_code=404, detail="IP address not found")

    ip.deleted = True
    db.commit()

    log_action(db, action="delete", user_id=user["id"], ip_id=ip.id, details="Deleted IP")
    logger.info(f"IP {ip_id} soft-deleted by user {user['id']}")

    return


# ✅ Get all visible IPs - All roles
@router.get("/", response_model=list[IPOut])
def get_all_ips(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    logger.info(f"User {user['id']} fetching IPs with role {user['role']}")

    query = db.query(IPAddress).filter(IPAddress.deleted == False)

    # 🔁 Uncomment if only regular users should see their own IPs
    # if user["role"] != "admin":
    #     query = query.filter(IPAddress.created_by == user["id"])

    ips = query.offset(skip).limit(limit).all()
    logger.info(f"Returned {len(ips)} IPs for user {user['id']}")

    return ips
