from fastapi import APIRouter
from pydantic import BaseModel
from app.services.fcm_integration import send_fcm_notification, send_fcm_multicast

router = APIRouter()

class NotificationRequest(BaseModel):
    device_token: str
    title: str
    body: str
    data: dict = {}

class MulticastRequest(BaseModel):
    device_tokens: list
    title: str
    body: str
    data: dict = {}

@router.post("/send")
async def send_notification(notification: NotificationRequest):
    """Send push notification to single device"""
    result = await send_fcm_notification(
        device_token=notification.device_token,
        title=notification.title,
        body=notification.body,
        data=notification.data
    )
    return result

@router.post("/send-multicast")
async def send_multicast_notification(notification: MulticastRequest):
    """Send push notification to multiple devices"""
    result = await send_fcm_multicast(
        device_tokens=notification.device_tokens,
        title=notification.title,
        body=notification.body,
        data=notification.data
    )
    return result
