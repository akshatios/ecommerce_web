from sqlalchemy.orm import Session
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate
import uuid

def create_payment(db: Session, payment: PaymentCreate):
    db_payment = Payment(
        trip_id=payment.trip_id,
        rider_id=payment.rider_id,
        driver_id=payment.driver_id,
        amount=payment.amount,
        method=payment.method,
        status=PaymentStatus.PENDING
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()

def get_payment_by_trip(db: Session, trip_id: int):
    return db.query(Payment).filter(Payment.trip_id == trip_id).first()

def process_payment(db: Session, payment_id: int):
    """
    Simulate payment processing
    In production, this would call Stripe/Razorpay API
    """
    db_payment = get_payment(db, payment_id)
    if db_payment:
        db_payment.status = PaymentStatus.PROCESSING
        # Simulate external transaction ID
        db_payment.transaction_id = f"txn_{uuid.uuid4().hex[:12]}"
        db.commit()
        
        # Simulate success (in reality, wait for webhook)
        db_payment.status = PaymentStatus.COMPLETED
        db.commit()
        db.refresh(db_payment)
    return db_payment
