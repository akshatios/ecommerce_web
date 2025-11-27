from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.crud import payment as crud_payment
from app.services.stripe_integration import create_payment_intent, confirm_payment, create_refund

router = APIRouter()

@router.post("/", response_model=PaymentResponse)
def create_payment_record(payment: PaymentCreate, db: Session = Depends(get_db)):
    """Create payment record and Stripe payment intent"""
    # Create payment record
    db_payment = crud_payment.create_payment(db=db, payment=payment)
    
    # Create Stripe payment intent
    try:
        intent = create_payment_intent(payment.amount)
        db_payment.transaction_id = intent["id"]
        db.commit()
        db.refresh(db_payment)
    except Exception as e:
        print(f"Payment intent creation failed: {e}")
    
    return db_payment

@router.post("/{payment_id}/process", response_model=PaymentResponse)
def process_payment_request(payment_id: int, db: Session = Depends(get_db)):
    """Process payment via Stripe"""
    payment = crud_payment.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Confirm payment with Stripe
    try:
        result = confirm_payment(payment.transaction_id)
        if result["status"] == "succeeded":
            payment = crud_payment.process_payment(db, payment_id)
    except Exception as e:
        print(f"Payment processing failed: {e}")
        payment.status = "FAILED"
        db.commit()
    
    return payment

@router.post("/{payment_id}/refund")
def refund_payment(payment_id: int, amount: float = None, db: Session = Depends(get_db)):
    """Refund a payment"""
    payment = crud_payment.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    try:
        result = create_refund(payment.transaction_id, amount)
        if result["status"] == "succeeded":
            payment.status = "REFUNDED"
            db.commit()
            return {"message": "Refund successful", "refund_id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Refund failed: {str(e)}")

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment_details(payment_id: int, db: Session = Depends(get_db)):
    payment = crud_payment.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/trip/{trip_id}", response_model=PaymentResponse)
def get_payment_by_trip(trip_id: int, db: Session = Depends(get_db)):
    payment = crud_payment.get_payment_by_trip(db, trip_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found for this trip")
    return payment
