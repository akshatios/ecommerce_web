from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.trip import TripRequest, TripResponse
from app.crud import trip as crud_trip
from app.services.matching import find_nearby_drivers
from app.services.websocket import manager
import json

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle subscription to trip updates
            if message.get("type") == "subscribe_trip":
                trip_id = message.get("trip_id")
                manager.subscribe_to_trip(user_id, trip_id)
                await manager.send_personal_message({
                    "type": "subscribed",
                    "trip_id": trip_id
                }, user_id)
            
            # Echo for testing
            elif message.get("type") == "ping":
                await manager.send_personal_message({
                    "type": "pong"
                }, user_id)
                
    except WebSocketDisconnect:
        manager.disconnect(user_id)

@router.post("/request", response_model=TripResponse)
async def request_trip(trip: TripRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Create Trip Record
    db_trip = crud_trip.create_trip(db, trip)
    
    # 2. Find Drivers (Async)
    drivers = await find_nearby_drivers(trip.pickup_lat, trip.pickup_lng)
    
    if drivers:
        # Simple matching: Pick the first one
        nearest_driver = drivers[0]
        crud_trip.assign_driver(db, db_trip.id, nearest_driver["driver_id"])
        
        # Broadcast trip assignment via WebSocket
        await manager.broadcast_to_trip({
            "type": "trip_assigned",
            "trip_id": db_trip.id,
            "driver_id": nearest_driver["driver_id"],
            "distance_km": nearest_driver["distance_km"]
        }, db_trip.id)
        
    return db_trip

@router.get("/{trip_id}", response_model=TripResponse)
def get_trip_details(trip_id: int, db: Session = Depends(get_db)):
    trip = crud_trip.get_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.post("/{trip_id}/start")
async def start_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = crud_trip.get_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    trip.status = "STARTED"
    db.commit()
    
    # Broadcast via WebSocket
    await manager.broadcast_to_trip({
        "type": "trip_started",
        "trip_id": trip_id
    }, trip_id)
    
    return {"message": "Trip started", "trip_id": trip_id}

@router.post("/{trip_id}/complete")
async def complete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = crud_trip.get_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    trip.status = "COMPLETED"
    db.commit()
    
    # Broadcast via WebSocket
    await manager.broadcast_to_trip({
        "type": "trip_completed",
        "trip_id": trip_id
    }, trip_id)
    
    return {"message": "Trip completed", "trip_id": trip_id}
