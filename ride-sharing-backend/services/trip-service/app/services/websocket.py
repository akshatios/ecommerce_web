from typing import Dict, Set
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        # Store active connections: {user_id: websocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # Store trip subscriptions: {trip_id: set of user_ids}
        self.trip_subscriptions: Dict[int, Set[str]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Remove from all trip subscriptions
        for trip_id in list(self.trip_subscriptions.keys()):
            if user_id in self.trip_subscriptions[trip_id]:
                self.trip_subscriptions[trip_id].remove(user_id)
                if not self.trip_subscriptions[trip_id]:
                    del self.trip_subscriptions[trip_id]

    def subscribe_to_trip(self, user_id: str, trip_id: int):
        if trip_id not in self.trip_subscriptions:
            self.trip_subscriptions[trip_id] = set()
        self.trip_subscriptions[trip_id].add(user_id)

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(json.dumps(message))

    async def broadcast_to_trip(self, message: dict, trip_id: int):
        if trip_id in self.trip_subscriptions:
            for user_id in self.trip_subscriptions[trip_id]:
                await self.send_personal_message(message, user_id)

manager = ConnectionManager()
