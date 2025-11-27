from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
import enum
from datetime import datetime
from app.core.database import Base

class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class PaymentMethod(str, enum.Enum):
    CARD = "CARD"
    WALLET = "WALLET"
    UPI = "UPI"
    CASH = "CASH"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, index=True, nullable=False)
    rider_id = Column(Integer, index=True, nullable=False)
    driver_id = Column(Integer, index=True, nullable=False)
    
    amount = Column(Float, nullable=False)
    method = Column(String, default=PaymentMethod.CARD)
    status = Column(String, default=PaymentStatus.PENDING)
    
    transaction_id = Column(String, unique=True, nullable=True)  # External payment gateway ID
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
