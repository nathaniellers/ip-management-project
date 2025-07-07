from fastapi import APIRouter, Header, Depends, Query
from app.dependencies import get_current_user
from app.schemas import IPCreate, IPUpdate, IPOut
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from app.services import get_all_ip_address, create_ip_address, update_ip_address, delete_ip_address

router = APIRouter(prefix="/api/ip", tags=["IP Management"])

@router.post("/", response_model=IPOut, status_code=201)
async def create_ip(
	data: IPCreate,
	db: Session = Depends(get_db),
	user=Depends(get_current_user),
	authorization: str = Header(...)
):
	return await create_ip_address(
		data,
		db,
		user,
		authorization
	)

@router.put("/{ip_id}", response_model=IPOut)
async def update_ip(
	ip_id: UUID,
	data: IPUpdate,
	db: Session = Depends(get_db),
	user=Depends(get_current_user)
):
	return await update_ip_address(
		ip_id,
		data,
		db,
		user
	)

@router.delete("/{ip_id}", status_code=204)
async def delete_ip(
	ip_id: UUID,
	db: Session = Depends(get_db),
	user=Depends(get_current_user)
):
	return await delete_ip_address(
		ip_id,
		db,
		user
	)

@router.get("/", summary="Get all IPs with pagination")
async def get_all_ips(
	skip: int = Query(0, ge=0),
	limit: int = Query(10, le=100),
	search: str = Query(None),
	db: Session = Depends(get_db),
	user=Depends(get_current_user)
):
	return await get_all_ip_address(
		skip,
		limit,
		search,
		db,
		user
	)

