from sqlalchemy.orm import Session
from app.models.trip import Trip, TripStatus
from app.schemas.trip import TripRequest

def create_trip(db: Session, trip: TripRequest):
    db_trip = Trip(
        rider_id=trip.rider_id,
        pickup_lat=trip.pickup_lat,
        pickup_lng=trip.pickup_lng,
        dropoff_lat=trip.dropoff_lat,
        dropoff_lng=trip.dropoff_lng,
        status=TripStatus.REQUESTED
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

def get_trip(db: Session, trip_id: int):
    return db.query(Trip).filter(Trip.id == trip_id).first()

def assign_driver(db: Session, trip_id: int, driver_id: int):
    db_trip = get_trip(db, trip_id)
    if db_trip:
        db_trip.driver_id = driver_id
        db_trip.status = TripStatus.ASSIGNED
        db.commit()
        db.refresh(db_trip)
    return db_trip
