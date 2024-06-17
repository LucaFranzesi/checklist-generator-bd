#region ------- IMPORTS -------------------------------------------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- CONSTANTS -----------------------------------------------------------------------------------

# Default value to use when not running inside Docker
DEFAULT_DB_URL = "postgresql://lucaf:1234@localhost:5432/checklist"

# TODO: Add a DB instance for testing purposes

# Get the DATABASE_URL from environment, or use the default value
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

#endregion ---- CONSTANTS -----------------------------------------------------------------------------------

#region ------- INIT ----------------------------------------------------------------------------------------

# Initialize database configuration
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#endregion ---- INIT ----------------------------------------------------------------------------------------

#region ------- UTILITY -------------------------------------------------------------------------------------

def get_db():
    """
    Returns an instance of the db for Database operations
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#endregion ---- UTILITY -------------------------------------------------------------------------------------