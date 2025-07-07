from fastapi import Header, HTTPException
from sqlalchemy.orm import Session
from app.models import IPAddress
from app.schemas import IPCreate, IPUpdate, IPOut
from uuid import UUID
from datetime import datetime
from app.queue.audit_queue import enqueue_audit_log
from app.utils.token import decode_token
import logging

logger = logging.getLogger(__name__)

async def create_ip_address(
	data: IPCreate,
	db: Session,
	user,
	authorization: str = Header(...)
):

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

	user_data = decode_token(authorization)
	user_info = user_data.get("user")

	await enqueue_audit_log({
		"actor_id": user_info["id"],
		"name": user_info["name"],
		"action": "create",
		"resource": "ip",
		"ip": data.ip,
		"session_id": user_info["session_id"],
		"details": f"Created IP: {data.ip}"
	})

	return new_ip


async def update_ip_address(ip_id: UUID, data: IPUpdate, db: Session, user):
	ip = db.query(IPAddress).filter(IPAddress.id == ip_id, IPAddress.deleted == False).first()
	if not ip:
		raise HTTPException(status_code=404, detail="IP address not found")
		
	if user["role"] != "admin" and ip.created_by != UUID(user["id"]):
		raise HTTPException(status_code=403, detail="Not authorized to update this IP")
	
	existing_ip_str = ip.ip

	ip.label = data.label
	ip.comment = data.comment
	ip.updated_at = datetime.utcnow()
	db.commit()

	await enqueue_audit_log({
		"actor_id": user["id"],
		"name": user["name"],
		"action": "update",
		"resource": "ip",
		"ip": existing_ip_str,
		"session_id": user["session_id"],
		"details": f"Updated IP: {existing_ip_str}"
	})

	return IPOut.model_validate(ip)



async def delete_ip_address(ip_id: UUID, db: Session, user):
	if user["role"] != "admin":
		raise HTTPException(status_code=403, detail="Only admins can delete IPs")

	ip = db.query(IPAddress).filter(IPAddress.id == ip_id, IPAddress.deleted == False).first()
	if not ip:
		raise HTTPException(status_code=404, detail="IP address not found")

	await enqueue_audit_log({
		"actor_id": user["id"],
		"name": user["name"],
		"action": "create",
		"resource": "ip",
		"ip": ip_id,
		"session_id": user["session_id"],
		"details": f"Deleted IP: {ip_id}"
	})
	ip.deleted = True
	db.commit()
	
	return

async def get_all_ip_address(skip: int, limit: int, search: str, db: Session, user):
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
