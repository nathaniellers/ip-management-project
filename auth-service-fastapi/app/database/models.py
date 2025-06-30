import uuid
from enum import Enum
from sqlalchemy import Column, String, Boolean, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from app.database.db import Base

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    role = Column(SqlEnum(UserRole, name="user_role"), nullable=False, default=UserRole.USER)
