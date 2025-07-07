from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.config import Settings

# ✔ Import models BEFORE setting target_metadata
from app import models  # <-- This is the file where your User model is defined
from app.database import Base  # <-- This is the correct Base class used by your models

config = context.config
fileConfig(config.config_file_name)

# Get DB URL from env vars
settings = Settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# ✔ This now includes all imported models (e.g., User)
target_metadata = Base.metadata


def run_migrations_online():
	connectable = engine_from_config(
		config.get_section(config.config_ini_section),
		prefix='sqlalchemy.',
		poolclass=pool.NullPool,
	)

	with connectable.connect() as connection:
		context.configure(connection=connection, target_metadata=target_metadata)
		with context.begin_transaction():
			context.run_migrations()


run_migrations_online()
