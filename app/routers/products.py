from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core import database
from app import schemas, oauth2
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/products",
    tags=['Products']
)

@router.get("/", response_model=List[schemas.ProductResponse])
def get_products(limit: int = 10, skip: int = 0):
    products = list(database.db.products.find().skip(skip).limit(limit))
    for product in products:
        product["id"] = str(product["_id"])
    return products

@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, current_user: dict = Depends(oauth2.get_current_user)):
    new_product = product.dict()
    new_product["created_at"] = datetime.utcnow()
    result = database.db.products.insert_one(new_product)
    new_product["id"] = str(result.inserted_id)
    return new_product

@router.get("/{id}", response_model=schemas.ProductResponse)
def get_product(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="Invalid ID")
        
    product = database.db.products.find_one({"_id": ObjectId(id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    product["id"] = str(product["_id"])
    return product

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: str, current_user: dict = Depends(oauth2.get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="Invalid ID")
        
    result = database.db.products.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return
