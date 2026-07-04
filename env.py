import os
import logging
from sqlalchemy import engine_from_config, pool
from alembic import context
from database.models import Base

# Alembic Config object, provides access to values within the .ini file
config = context.config

# Interpret the config file for Python logging
logging.basicConfig()
logger = logging.getLogger('alembic.env')

# Retrieve the database URL from the environment variable
DATABASE_URL_ENV = "DATABASE_URL"
database_url = os.environ.get(DATABASE_URL_ENV)
if not database_url:
    raise RuntimeError(f"Environment variable {DATABASE_URL_ENV} is not set.")

# Set the SQLAlchemy URL in the Alembic config
config.set_main_option("sqlalchemy.url", database_url)

# Target metadata for Alembic migrations
target_metadata = Base.metadata