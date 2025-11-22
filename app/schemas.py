from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    image_url: Optional[str] = None
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str
    created_at: datetime

# Order Schemas
class OrderItem(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]
    total_amount: float

class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: str
    created_at: datetime
