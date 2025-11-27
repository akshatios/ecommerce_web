from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False) # Link to Auth Service User ID
    license_number = Column(String, unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    rating = Column(Float, default=5.0)
    
    vehicle = relationship("Vehicle", back_populates="driver", uselist=False)

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    make = Column(String)
    model = Column(String)
    plate_number = Column(String, unique=True)
    color = Column(String)
    
    driver = relationship("Driver", back_populates="vehicle")
