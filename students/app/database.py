import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_models import Base

engine = create_engine(os.getenv("ENGINE_URL", "sqlite:///./students.db"))
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
