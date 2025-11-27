from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, verify_password, verify_token
from app.schemas.user import UserCreate, UserResponse, Token, OTPRequest, OTPVerify, RefreshTokenRequest
from app.crud import user as crud_user
from app.services.otp import generate_otp, store_otp, verify_otp, send_otp_sms

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register new user with email/password or phone"""
    if user.email:
        db_user = crud_user.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    if user.phone:
        db_user = crud_user.get_user_by_phone(db, phone=user.phone)
        if db_user:
            raise HTTPException(status_code=400, detail="Phone already registered")
    
    return crud_user.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login with email and password"""
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    # Store refresh token in database
    crud_user.store_refresh_token(db, user.id, refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/otp/request")
def request_otp(request: OTPRequest, db: Session = Depends(get_db)):
    """Request OTP for phone number"""
    # Check if user exists, if not create a placeholder
    user = crud_user.get_user_by_phone(db, phone=request.phone)
    if not user:
        # Create user with phone only
        user_create = UserCreate(phone=request.phone, full_name="User")
        user = crud_user.create_user(db, user_create)
    
    # Generate and send OTP
    otp = generate_otp()
    store_otp(request.phone, otp)
    send_otp_sms(request.phone, otp)
    
    return {"message": "OTP sent successfully", "phone": request.phone}

@router.post("/otp/verify", response_model=Token)
def verify_otp_login(request: OTPVerify, db: Session = Depends(get_db)):
    """Verify OTP and login"""
    if not verify_otp(request.phone, request.otp):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP"
        )
    
    # Get user by phone
    user = crud_user.get_user_by_phone(db, phone=request.phone)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate tokens
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    # Store refresh token
    crud_user.store_refresh_token(db, user.id, refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_access_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    # Verify refresh token
    user_id = verify_token(request.refresh_token, token_type="refresh")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Check if token exists and is not revoked
    db_token = crud_user.verify_refresh_token(db, request.refresh_token)
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired or revoked"
        )
    
    # Generate new tokens
    access_token = create_access_token(subject=user_id)
    new_refresh_token = create_refresh_token(subject=user_id)
    
    # Revoke old refresh token and store new one
    crud_user.revoke_refresh_token(db, request.refresh_token)
    crud_user.store_refresh_token(db, int(user_id), new_refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Logout by revoking refresh token"""
    crud_user.revoke_refresh_token(db, request.refresh_token)
    return {"message": "Logged out successfully"}
