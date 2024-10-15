from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Path to your SQLite database
DATABASE_PATH = '/Users/andylee/Projects/logan/data/logan_database_prototype.db'

# Create an SQLite database engine
engine = create_engine(f'sqlite:///{DATABASE_PATH}')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Initialize the database (create tables if they don't exist)
def init_db():
    Base.metadata.create_all(engine)
