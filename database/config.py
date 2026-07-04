import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from database.models import Base

# Read DATABASE_URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

# Configure SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

# Scoped session for thread safety
ScopedSession = scoped_session(SessionLocal)

def get_db():
    db = ScopedSession()
    try:
        yield db
    finally:
        db.close()