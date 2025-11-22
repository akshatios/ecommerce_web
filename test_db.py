
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from app import utils
import sys

# Add current directory to sys.path so we can import app
sys.path.append(os.getcwd())

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print(f"MONGO_URI: {MONGO_URI}")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    client.server_info() # Force connection
    print("MongoDB connection successful")
    db = client.ecommerce_db
    print("Database selected")
except Exception as e:
    print(f"MongoDB connection failed: {e}")

try:
    hash = utils.get_password_hash("testpassword")
    print(f"Password hashing successful: {hash[:10]}...")
except Exception as e:
    print(f"Password hashing failed: {e}")
