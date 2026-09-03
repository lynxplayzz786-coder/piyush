import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "progress.db")

turso_url = os.environ.get("TURSO_DATABASE_URL", "libsql://database-abhishek-ve.aws-ap-south-1.turso.io")
turso_token = os.environ.get("TURSO_AUTH_TOKEN")

if turso_url and turso_token:
    # Vercel / Cloud mode
    DATABASE_URL = turso_url.replace("libsql://", "sqlite+libsql://")
    engine = create_engine(
        f"{DATABASE_URL}/?secure=true", 
        connect_args={
            "check_same_thread": False, 
            "auth_token": turso_token
        }
    )
else:
    # Local mode fallback
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
