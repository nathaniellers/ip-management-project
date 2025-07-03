from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import IPAddress, AuditLog
from app.schemas import IPCreate, IPUpdate, IPOut, AuditLogOut
from uuid import UUID
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def create_ip(data: IPCreate, db: Session, user):
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
	return new_ip


def update_ip(ip_id: UUID, data: IPUpdate, db: Session, user):
	ip = db.query(IPAddress).filter(IPAddress.id == ip_id, IPAddress.deleted == False).first()
	if not ip:
		raise HTTPException(status_code=404, detail="IP address not found")

	if user["role"] != "admin" and ip.created_by != user["id"]:
		raise HTTPException(status_code=403, detail="Not authorized to update this IP")

	ip.label = data.label
	ip.comment = data.comment
	ip.updated_at = datetime.utcnow()
	db.commit()
	return IPOut.model_validate(ip)


def delete_ip(ip_id: UUID, db: Session, user):
	if user["role"] != "admin":
		raise HTTPException(status_code=403, detail="Only admins can delete IPs")

	ip = db.query(IPAddress).filter(IPAddress.id == ip_id, IPAddress.deleted == False).first()
	if not ip:
		raise HTTPException(status_code=404, detail="IP address not found")

	ip.deleted = True
	db.commit()
	return


def get_all_ips(skip: int, limit: int, search: str, db: Session, user):
	query = db.query(IPAddress).filter(IPAddress.deleted == False)
	if search:
		query = query.filter(
			IPAddress.ip.ilike(f"%{search}%") |
			IPAddress.label.ilike(f"%{search}%") |
			IPAddress.comment.ilike(f"%{search}%")
		)
	total = query.count()
	ips = query.offset(skip).limit(limit).all()
	return {
		"total": total,
		"data": [IPOut.model_validate(ip).model_dump() for ip in ips]
	}
