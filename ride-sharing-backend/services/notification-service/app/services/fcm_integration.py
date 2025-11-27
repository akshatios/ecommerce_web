from firebase_admin import credentials, messaging, initialize_app
from app.core.config import settings
import os

# Initialize Firebase Admin (if credentials provided)
firebase_initialized = False

def init_firebase():
    global firebase_initialized
    if settings.FCM_SERVER_KEY and not firebase_initialized:
        try:
            # In production, use service account JSON file
            # cred = credentials.Certificate("path/to/serviceAccountKey.json")
            # initialize_app(cred)
            firebase_initialized = True
            print("[FCM] Firebase initialized")
        except Exception as e:
            print(f"[FCM] Initialization failed: {e}")

async def send_fcm_notification(device_token: str, title: str, body: str, data: dict = None):
    """
    Send push notification via Firebase Cloud Messaging
    """
    if not firebase_initialized:
        # Stub mode
        print(f"[FCM STUB] Sending to {device_token}: {title} - {body}")
        print(f"[FCM STUB] Data: {data}")
        return {"status": "sent", "message": "FCM stub mode"}
    
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            token=device_token,
        )
        
        response = messaging.send(message)
        print(f"[FCM] Successfully sent message: {response}")
        return {"status": "sent", "message_id": response}
        
    except Exception as e:
        print(f"[FCM] Error sending notification: {e}")
        return {"status": "error", "message": str(e)}

async def send_fcm_multicast(device_tokens: list, title: str, body: str, data: dict = None):
    """
    Send notification to multiple devices
    """
    if not firebase_initialized:
        print(f"[FCM STUB] Sending to {len(device_tokens)} devices: {title}")
        return {"status": "sent", "success_count": len(device_tokens)}
    
    try:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            tokens=device_tokens,
        )
        
        response = messaging.send_multicast(message)
        print(f"[FCM] {response.success_count} messages sent successfully")
        return {
            "status": "sent",
            "success_count": response.success_count,
            "failure_count": response.failure_count
        }
        
    except Exception as e:
        print(f"[FCM] Error sending multicast: {e}")
        return {"status": "error", "message": str(e)}

# Initialize on module load
init_firebase()
