from sqlalchemy.orm import Session
from app.models.driver import Driver, Vehicle
from app.schemas.driver import DriverCreate

def get_driver(db: Session, driver_id: int):
    return db.query(Driver).filter(Driver.id == driver_id).first()

def get_driver_by_user_id(db: Session, user_id: int):
    return db.query(Driver).filter(Driver.user_id == user_id).first()

def create_driver(db: Session, driver: DriverCreate):
    db_driver = Driver(
        user_id=driver.user_id,
        license_number=driver.license_number
    )
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)

    db_vehicle = Vehicle(
        driver_id=db_driver.id,
        **driver.vehicle.dict()
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    
    return db_driver
