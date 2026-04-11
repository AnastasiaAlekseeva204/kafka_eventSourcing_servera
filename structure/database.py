import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from structure.database_models import Base

DATABASE_URL = os.getenv("ENGINE_URL")

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)