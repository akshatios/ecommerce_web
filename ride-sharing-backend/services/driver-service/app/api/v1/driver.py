from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.driver import DriverCreate, DriverResponse
from app.crud import driver as crud_driver

router = APIRouter()

@router.post("/", response_model=DriverResponse)
def create_driver_profile(driver: DriverCreate, db: Session = Depends(get_db)):
    db_driver = crud_driver.get_driver_by_user_id(db, user_id=driver.user_id)
    if db_driver:
        raise HTTPException(status_code=400, detail="Driver profile already exists for this user")
    return crud_driver.create_driver(db=db, driver=driver)

@router.get("/{driver_id}", response_model=DriverResponse)
def read_driver(driver_id: int, db: Session = Depends(get_db)):
    db_driver = crud_driver.get_driver(db, driver_id=driver_id)
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_driver
