from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import database, schemas, utils
from bson import ObjectId

router = APIRouter(tags=['Authentication'])

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate):
    existing_user = database.db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = utils.get_password_hash(user.password)
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "is_active": True
    }
    result = database.db.users.insert_one(new_user)
    new_user["id"] = str(result.inserted_id)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = database.db.users.find_one({"username": user_credentials.username})
    
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user['password']):
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    
    access_token = utils.create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}
