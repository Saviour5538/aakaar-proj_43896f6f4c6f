import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.config import get_db, engine
from backend.routes.auth import router as auth_router
from backend.routes.documents import router as documents_router
from backend.routes.conversations import router as conversations_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    from database.models import Base
    
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Register pgvector adapter if using psycopg2
    try:
        from pgvector.psycopg2 import register_vector
        import psycopg2
        
        # Get raw psycopg2 connection from engine
        with engine.connect() as conn:
            # Get the underlying psycopg2 connection
            raw_conn = conn.connection
            register_vector(raw_conn)
    except ImportError:
        pass  # pgvector not installed or not using psycopg2
    except Exception as e:
        print(f"Warning: Could not register pgvector adapter: {e}")
    
    yield
    
    # Shutdown
    pass  # Add any necessary cleanup logic here

# Initialize FastAPI app
app = FastAPI(
    title="DocMind",
    description="AI-powered document management and conversational assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(conversations_router, prefix="/api")

# Auto-mounted AI router — ai/routes.py exposes /api/ai/* (it carries its own prefix)
try:
    from ai.routes import router as ai_router
    app.include_router(ai_router)
except ImportError as e:
    print(f"Warning: AI router not loaded: {e}")