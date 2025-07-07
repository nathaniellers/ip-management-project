from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime
from app.database import Base

class IPAddress(Base):
	__tablename__ = "ip_addresses"

	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
	ip = Column(String, nullable=False)
	label = Column(String, nullable=True)
	comment = Column(String, nullable=True)
	created_by = Column(UUID(as_uuid=True), nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
	deleted = Column(Boolean, default=False)