from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core import database
from app import schemas, oauth2
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)

@router.post("/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, current_user: dict = Depends(oauth2.get_current_user)):
    new_order = order.dict()
    new_order["user_id"] = str(current_user["_id"])
    new_order["created_at"] = datetime.utcnow()
    new_order["status"] = "pending"
    
    # Verify products exist and calculate total (optional validation)
    # For simplicity, we trust the input total or recalculate it here
    
    result = database.db.orders.insert_one(new_order)
    new_order["id"] = str(result.inserted_id)
    return new_order

@router.get("/", response_model=List[schemas.OrderResponse])
def get_orders(current_user: dict = Depends(oauth2.get_current_user)):
    orders = list(database.db.orders.find({"user_id": str(current_user["_id"])}))
    for order in orders:
        order["id"] = str(order["_id"])
    return orders
