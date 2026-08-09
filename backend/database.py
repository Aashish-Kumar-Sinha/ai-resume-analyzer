from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite connection URL
DATABASE_URL = "sqlite:///./ats_database.db"

# Create the engine. check_same_thread=False is required for SQLite in FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory for handling requests
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()

# Reusable database session dependency for endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()