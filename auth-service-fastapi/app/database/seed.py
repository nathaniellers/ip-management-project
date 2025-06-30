from app.database.db import SessionLocal
from app.database.models import User
from passlib.context import CryptContext
import uuid

# Initialize DB session and password hasher
db = SessionLocal()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration
DEFAULT_ADMIN_EMAIL = "nathanielleromero18@gmail.com"
DEFAULT_ADMIN_PASSWORD = "password"
DEFAULT_ADMIN_NAME = "Super Admin"
DEFAULT_ADMIN_ROLE = "admin"

existing_user = db.query(User).filter(User.email == DEFAULT_ADMIN_EMAIL).first()
if not existing_user:
    print("Creating default admin user...")
    admin = User(
        id=uuid.uuid4(),
        email=DEFAULT_ADMIN_EMAIL,
        hashed_password=pwd_context.hash(DEFAULT_ADMIN_PASSWORD),
        full_name=DEFAULT_ADMIN_NAME,
        role=DEFAULT_ADMIN_ROLE,
        disabled=False
    )
    db.add(admin)
    db.commit()
    print(f"Admin user {DEFAULT_ADMIN_EMAIL} created!")
else:
    print(f"Admin user {DEFAULT_ADMIN_EMAIL} already exists.")

db.close()
