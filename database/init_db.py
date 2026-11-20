"""
Initialize Database
"""

from database.db import Base
from database.db import engine

# Import all models
import database.models

Base.metadata.create_all(bind=engine)

print("Database created successfully.")