#!/usr/bin/env python3
"""
Database initialization script
Run this to create all tables in the database
"""
import sys
sys.path.append('.')

from app.core.database import engine, Base
from app.models.user import User, RefreshToken

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_db()
