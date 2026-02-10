from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} # Only needed for SQLite
)

SessionLocal = sessionmaker(bind = engine)

Base = declarative_base()