import random
import redis
from datetime import timedelta
from app.core.config import settings
from app.core.redis import get_redis

# For production, use Twilio
# from twilio.rest import Client

def generate_otp() -> str:
    """Generate 6-digit OTP"""
    return str(random.randint(100000, 999999))

def store_otp(phone: str, otp: str) -> None:
    """Store OTP in Redis with expiration"""
    redis_client = get_redis()
    key = f"otp:{phone}"
    redis_client.setex(key, timedelta(minutes=settings.OTP_EXPIRE_MINUTES), otp)

def verify_otp(phone: str, otp: str) -> bool:
    """Verify OTP from Redis"""
    redis_client = get_redis()
    key = f"otp:{phone}"
    stored_otp = redis_client.get(key)
    
    if stored_otp and stored_otp == otp:
        redis_client.delete(key)  # Delete after successful verification
        return True
    return False

def send_otp_sms(phone: str, otp: str) -> bool:
    """
    Send OTP via SMS using Twilio
    For development, just print to console
    """
    # Development mode - just log
    print(f"[OTP] Sending OTP {otp} to {phone}")
    
    # Production mode - uncomment below
    # try:
    #     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    #     message = client.messages.create(
    #         body=f"Your ride-sharing OTP is: {otp}. Valid for {settings.OTP_EXPIRE_MINUTES} minutes.",
    #         from_=settings.TWILIO_PHONE_NUMBER,
    #         to=phone
    #     )
    #     return True
    # except Exception as e:
    #     print(f"Error sending OTP: {e}")
    #     return False
    
    return True
