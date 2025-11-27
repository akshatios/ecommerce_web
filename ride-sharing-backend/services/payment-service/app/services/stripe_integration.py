import stripe
from app.core.config import settings

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount: float, currency: str = "usd") -> dict:
    """
    Create a Stripe payment intent
    """
    if not settings.STRIPE_SECRET_KEY:
        # Stub mode
        return {
            "id": f"pi_stub_{int(amount * 100)}",
            "client_secret": "stub_client_secret",
            "status": "requires_payment_method"
        }
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency,
            automatic_payment_methods={"enabled": True},
        )
        return {
            "id": intent.id,
            "client_secret": intent.client_secret,
            "status": intent.status
        }
    except Exception as e:
        print(f"Stripe error: {e}")
        raise

def confirm_payment(payment_intent_id: str) -> dict:
    """
    Confirm a payment intent
    """
    if not settings.STRIPE_SECRET_KEY:
        # Stub mode
        return {
            "id": payment_intent_id,
            "status": "succeeded"
        }
    
    try:
        intent = stripe.PaymentIntent.confirm(payment_intent_id)
        return {
            "id": intent.id,
            "status": intent.status
        }
    except Exception as e:
        print(f"Stripe error: {e}")
        raise

def create_refund(payment_intent_id: str, amount: float = None) -> dict:
    """
    Create a refund
    """
    if not settings.STRIPE_SECRET_KEY:
        # Stub mode
        return {
            "id": f"re_stub_{payment_intent_id}",
            "status": "succeeded"
        }
    
    try:
        refund_params = {"payment_intent": payment_intent_id}
        if amount:
            refund_params["amount"] = int(amount * 100)
        
        refund = stripe.Refund.create(**refund_params)
        return {
            "id": refund.id,
            "status": refund.status
        }
    except Exception as e:
        print(f"Stripe error: {e}")
        raise
