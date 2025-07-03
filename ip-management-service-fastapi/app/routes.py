from fastapi import APIRouter, Depends, Query
from app.dependencies import get_db, get_current_user
from app.schemas import IPCreate, IPUpdate, IPOut
from sqlalchemy.orm import Session
from uuid import UUID
from app.services import get_all_ips, create_ip, update_ip, delete_ip

router = APIRouter(prefix="/api/ip", tags=["IP Management"])

@router.post("/", response_model=IPOut, status_code=201)
def create_ip(
		data: IPCreate,
		db: Session = Depends(get_db),
		user=Depends(get_current_user)
	):
	return create_ip(
		data,
		db,
		user
	)

@router.put("/{ip_id}", response_model=IPOut)
def update_ip(
		ip_id: UUID,
		data: IPUpdate,
		db: Session = Depends(get_db),
		user=Depends(get_current_user)
	):
	
	return update_ip(
		ip_id,
		data,
		db,
		user
	)

@router.delete("/{ip_id}", status_code=204)
def delete_ip(
		ip_id: UUID,
		db: Session = Depends(get_db),
		user=Depends(get_current_user)
	):
	return delete_ip(
		ip_id,
		db,
		user
	)

@router.get("/", summary="Get all IPs with pagination")
def get_all_ips(
		skip: int = Query(0, ge=0),
		limit: int = Query(10, le=100),
		search: str = Query(None),
		db: Session = Depends(get_db),
		user=Depends(get_current_user)
	):
	
	return get_all_ips(
		skip,
		limit,
		search,
		db,
		user
	)

