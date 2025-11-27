from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.rider import RiderCreate, RiderResponse
from app.crud import rider as crud_rider

router = APIRouter()

@router.post("/", response_model=RiderResponse)
def create_rider_profile(rider: RiderCreate, db: Session = Depends(get_db)):
    db_rider = crud_rider.get_rider_by_user_id(db, user_id=rider.user_id)
    if db_rider:
        raise HTTPException(status_code=400, detail="Rider profile already exists for this user")
    return crud_rider.create_rider(db=db, rider=rider)

@router.get("/{rider_id}", response_model=RiderResponse)
def read_rider(rider_id: int, db: Session = Depends(get_db)):
    db_rider = crud_rider.get_rider(db, rider_id=rider_id)
    if db_rider is None:
        raise HTTPException(status_code=404, detail="Rider not found")
    return db_rider
