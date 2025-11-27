from sqlalchemy.orm import Session
from app.models.rider import Rider
from app.schemas.rider import RiderCreate

def get_rider(db: Session, rider_id: int):
    return db.query(Rider).filter(Rider.id == rider_id).first()

def get_rider_by_user_id(db: Session, user_id: int):
    return db.query(Rider).filter(Rider.user_id == user_id).first()

def create_rider(db: Session, rider: RiderCreate):
    db_rider = Rider(
        user_id=rider.user_id,
        phone=rider.phone
    )
    db.add(db_rider)
    db.commit()
    db.refresh(db_rider)
    return db_rider
