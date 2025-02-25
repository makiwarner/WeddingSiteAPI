from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import Column, Integer, String


# Get the database URL from an environment variable, or paste your Neon connection string directly
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_VpEZbPH52SDF@ep-red-voice-a8tbyl76-pooler.eastus2.azure.neon.tech/neondb?sslmode=require")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    number_of_invitees = Column(Integer)
    status = Column(String, nullable=True)
