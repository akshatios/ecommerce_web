from pymongo import MongoClient
from app.core.config import settings

class Database:
    """MongoDB database connection manager"""
    
    def __init__(self):
        self.client = None
        self.db = None
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(settings.MONGO_URI)
            # Extract database name from URI or use default
            if "mongodb+srv://" in settings.MONGO_URI or "mongodb://" in settings.MONGO_URI:
                # Try to get database name from URI
                if "/" in settings.MONGO_URI.split("@")[-1]:
                    db_name = settings.MONGO_URI.split("@")[-1].split("/")[1].split("?")[0]
                    if db_name:
                        self.db = self.client[db_name]
                    else:
                        self.db = self.client[settings.DATABASE_NAME]
                else:
                    self.db = self.client[settings.DATABASE_NAME]
            else:
                self.db = self.client[settings.DATABASE_NAME]
            
            # Test connection
            self.client.server_info()
            print(f"✅ Connected to MongoDB: {self.db.name}")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            raise
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("🔌 MongoDB connection closed")
    
    def get_database(self):
        """Get database instance"""
        return self.db

# Create database instance
database = Database()
database.connect()

# Export db for backward compatibility
db = database.db
