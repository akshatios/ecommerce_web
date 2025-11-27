import math
from app.core.config import settings

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def calculate_fare(pickup_lat: float, pickup_lng: float, dropoff_lat: float, dropoff_lng: float, estimated_time_minutes: float = 0) -> dict:
    """
    Calculate fare based on distance and time
    """
    distance_km = haversine_distance(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)
    
    # If no time estimate provided, estimate based on distance (avg 30 km/h in city)
    if estimated_time_minutes == 0:
        estimated_time_minutes = (distance_km / 30) * 60
    
    # Calculate fare components
    base_fare = settings.BASE_FARE
    distance_fare = distance_km * settings.PER_KM_RATE
    time_fare = estimated_time_minutes * settings.PER_MINUTE_RATE
    
    # Apply surge pricing
    subtotal = base_fare + distance_fare + time_fare
    total_fare = subtotal * settings.SURGE_MULTIPLIER
    
    return {
        "distance_km": round(distance_km, 2),
        "estimated_time_minutes": round(estimated_time_minutes, 2),
        "base_fare": base_fare,
        "distance_fare": round(distance_fare, 2),
        "time_fare": round(time_fare, 2),
        "surge_multiplier": settings.SURGE_MULTIPLIER,
        "total_fare": round(total_fare, 2)
    }
