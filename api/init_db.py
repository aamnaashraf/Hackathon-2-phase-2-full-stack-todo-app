"""
Database initialization script for Todo Web Application
This script should be run separately to create the database tables
"""
import os
import sys
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

# Add the current directory to the Python path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import models
from index import User, Todo

def init_db():
    # Get database URL
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        DATABASE_URL = os.getenv("VERCEL_POSTGRES_URL")
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL or VERCEL_POSTGRES_URL not found in environment variables")

    # Create engine
    engine = create_engine(
        DATABASE_URL,
        echo=True  # Set to True to see SQL statements
    )

    # For PostgreSQL, we need to ensure proper table creation
    # Drop existing tables first (be careful with this in production!)
    from sqlalchemy import text

    print("Dropping existing tables (if any)...")
    try:
        with engine.connect() as conn:
            # Use transaction to ensure all operations are atomic
            with conn.begin():
                # Drop tables in correct order to respect foreign key constraints
                conn.execute(text("DROP TABLE IF EXISTS todo CASCADE"))
                conn.execute(text("DROP TABLE IF EXISTS \"user\" CASCADE"))
                # The priority enum type might also need to be dropped if it exists
                conn.execute(text("DROP TYPE IF EXISTS priority CASCADE"))
    except Exception as e:
        print(f"Warning: Could not drop existing tables: {e}")

    # Create all tables
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()