from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base

class Rider(Base):
    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)  # Link to Auth Service User ID
    phone = Column(String, unique=True, nullable=False)
    wallet_balance = Column(Float, default=0.0)
    rating = Column(Float, default=5.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
