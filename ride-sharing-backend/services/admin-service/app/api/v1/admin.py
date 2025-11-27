from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from datetime import datetime, timedelta
from typing import List

from app.core.database import get_db
from app.schemas.admin import DashboardStats, UserStats, TripStats, RevenueStats

router = APIRouter()

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get overall dashboard statistics"""
    
    # Count total users
    total_users = db.execute(text("SELECT COUNT(*) FROM users WHERE role='rider'")).scalar() or 0
    
    # Count total drivers
    total_drivers = db.execute(text("SELECT COUNT(*) FROM drivers")).scalar() or 0
    
    # Count total trips
    total_trips = db.execute(text("SELECT COUNT(*) FROM trips")).scalar() or 0
    
    # Count active trips
    active_trips = db.execute(text(
        "SELECT COUNT(*) FROM trips WHERE status IN ('REQUESTED', 'ASSIGNED', 'STARTED')"
    )).scalar() or 0
    
    # Calculate total revenue
    total_revenue = db.execute(text(
        "SELECT COALESCE(SUM(amount), 0) FROM payments WHERE status='COMPLETED'"
    )).scalar() or 0.0
    
    # Count today's trips
    today = datetime.utcnow().date()
    today_trips = db.execute(text(
        f"SELECT COUNT(*) FROM trips WHERE DATE(created_at) = '{today}'"
    )).scalar() or 0
    
    return {
        "total_users": total_users,
        "total_drivers": total_drivers,
        "total_trips": total_trips,
        "active_trips": active_trips,
        "total_revenue": float(total_revenue),
        "today_trips": today_trips
    }

@router.get("/users", response_model=List[UserStats])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users with pagination"""
    
    result = db.execute(text(
        f"SELECT * FROM users ORDER BY created_at DESC LIMIT {limit} OFFSET {skip}"
    ))
    
    users = []
    for row in result:
        users.append({
            "id": row.id,
            "email": row.email,
            "phone": row.phone,
            "full_name": row.full_name,
            "role": row.role,
            "is_active": row.is_active,
            "created_at": row.created_at
        })
    
    return users

@router.get("/trips", response_model=List[TripStats])
def get_all_trips(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all trips with optional status filter"""
    
    query = "SELECT * FROM trips"
    if status:
        query += f" WHERE status = '{status}'"
    query += f" ORDER BY created_at DESC LIMIT {limit} OFFSET {skip}"
    
    result = db.execute(text(query))
    
    trips = []
    for row in result:
        trips.append({
            "id": row.id,
            "rider_id": row.rider_id,
            "driver_id": row.driver_id,
            "status": row.status,
            "fare": row.fare,
            "created_at": row.created_at,
            "pickup_lat": row.pickup_lat,
            "pickup_lng": row.pickup_lng,
            "dropoff_lat": row.dropoff_lat,
            "dropoff_lng": row.dropoff_lng
        })
    
    return trips

@router.get("/revenue/daily", response_model=List[RevenueStats])
def get_daily_revenue(days: int = 7, db: Session = Depends(get_db)):
    """Get daily revenue stats for last N days"""
    
    stats = []
    for i in range(days):
        date = (datetime.utcnow() - timedelta(days=i)).date()
        
        # Count trips for this day
        trip_count = db.execute(text(
            f"SELECT COUNT(*) FROM trips WHERE DATE(created_at) = '{date}'"
        )).scalar() or 0
        
        # Sum revenue for this day
        revenue = db.execute(text(
            f"SELECT COALESCE(SUM(amount), 0) FROM payments "
            f"WHERE status='COMPLETED' AND DATE(created_at) = '{date}'"
        )).scalar() or 0.0
        
        avg_fare = revenue / trip_count if trip_count > 0 else 0.0
        
        stats.append({
            "date": str(date),
            "total_trips": trip_count,
            "total_revenue": float(revenue),
            "average_fare": float(avg_fare)
        })
    
    return stats

@router.post("/users/{user_id}/activate")
def activate_user(user_id: int, db: Session = Depends(get_db)):
    """Activate a user"""
    db.execute(text(f"UPDATE users SET is_active = true WHERE id = {user_id}"))
    db.commit()
    return {"message": "User activated"}

@router.post("/users/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    """Deactivate a user"""
    db.execute(text(f"UPDATE users SET is_active = false WHERE id = {user_id}"))
    db.commit()
    return {"message": "User deactivated"}

@router.post("/drivers/{driver_id}/verify")
def verify_driver(driver_id: int, db: Session = Depends(get_db)):
    """Verify a driver"""
    db.execute(text(f"UPDATE drivers SET is_verified = true WHERE id = {driver_id}"))
    db.commit()
    return {"message": "Driver verified"}

@router.delete("/trips/{trip_id}")
def cancel_trip(trip_id: int, db: Session = Depends(get_db)):
    """Cancel a trip (admin action)"""
    db.execute(text(f"UPDATE trips SET status = 'CANCELLED' WHERE id = {trip_id}"))
    db.commit()
    return {"message": "Trip cancelled"}

@router.get("/stats/realtime")
def get_realtime_stats(db: Session = Depends(get_db)):
    """Get real-time statistics"""
    
    # Active drivers (updated location in last 5 minutes)
    five_min_ago = datetime.utcnow() - timedelta(minutes=5)
    
    # Trips by status
    trips_by_status = {}
    result = db.execute(text(
        "SELECT status, COUNT(*) as count FROM trips GROUP BY status"
    ))
    for row in result:
        trips_by_status[row.status] = row.count
    
    # Revenue today
    today = datetime.utcnow().date()
    today_revenue = db.execute(text(
        f"SELECT COALESCE(SUM(amount), 0) FROM payments "
        f"WHERE status='COMPLETED' AND DATE(created_at) = '{today}'"
    )).scalar() or 0.0
    
    return {
        "trips_by_status": trips_by_status,
        "today_revenue": float(today_revenue),
        "timestamp": datetime.utcnow().isoformat()
    }
