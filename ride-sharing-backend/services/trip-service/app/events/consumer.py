from kafka import KafkaConsumer
import json
import threading
from app.core.config import settings

class EventConsumer:
    def __init__(self):
        self.consumers = {}
        
    def start_consumer(self, topic: str, callback):
        """Start a Kafka consumer in a background thread"""
        def consume():
            try:
                consumer = KafkaConsumer(
                    topic,
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(','),
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    group_id=f"{topic}_consumer_group"
                )
                
                print(f"[KAFKA] Started consumer for topic: {topic}")
                
                for message in consumer:
                    try:
                        callback(message.value)
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        
            except Exception as e:
                print(f"Kafka consumer error for {topic}: {e}")
        
        thread = threading.Thread(target=consume, daemon=True)
        thread.start()
        self.consumers[topic] = thread

event_consumer = EventConsumer()

# Example consumer callbacks
def handle_payment_processed(event: dict):
    print(f"[CONSUMER] Payment processed: {event}")
    # Update trip with payment status

def handle_driver_location_updated(event: dict):
    print(f"[CONSUMER] Driver location updated: {event}")
    # Update driver location in cache
