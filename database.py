from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Change this to your local postgres credentials
# DATABASE_URL = "postgresql://user:password@localhost:5432/truber_db"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./truber.db") # Defaulting to SQLite for easy start, switch to Postgres as needed

engine = create_engine(DATABASE_URL)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
