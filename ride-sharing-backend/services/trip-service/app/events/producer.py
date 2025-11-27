from kafka import KafkaProducer
import json
from app.core.config import settings

class EventProducer:
    def __init__(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(','),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except Exception as e:
            print(f"Kafka producer initialization failed: {e}")
            self.producer = None

    def publish_event(self, topic: str, event: dict):
        if self.producer:
            try:
                self.producer.send(topic, event)
                self.producer.flush()
                print(f"[KAFKA] Published to {topic}: {event}")
            except Exception as e:
                print(f"Error publishing event: {e}")
        else:
            print(f"[KAFKA DISABLED] Would publish to {topic}: {event}")

event_producer = EventProducer()

# Event publishing functions
def publish_trip_requested(trip_id: int, rider_id: int, pickup_lat: float, pickup_lng: float):
    event_producer.publish_event("trip.requested", {
        "trip_id": trip_id,
        "rider_id": rider_id,
        "pickup_lat": pickup_lat,
        "pickup_lng": pickup_lng,
        "timestamp": str(datetime.utcnow())
    })

def publish_trip_assigned(trip_id: int, driver_id: int):
    event_producer.publish_event("trip.assigned", {
        "trip_id": trip_id,
        "driver_id": driver_id,
        "timestamp": str(datetime.utcnow())
    })

def publish_trip_started(trip_id: int):
    event_producer.publish_event("trip.started", {
        "trip_id": trip_id,
        "timestamp": str(datetime.utcnow())
    })

def publish_trip_completed(trip_id: int, fare: float):
    event_producer.publish_event("trip.completed", {
        "trip_id": trip_id,
        "fare": fare,
        "timestamp": str(datetime.utcnow())
    })

from datetime import datetime
