"""
Database Schemas for Saaz International – Online Shopping

Each Pydantic model below corresponds to a MongoDB collection. The collection
name is the lowercase of the class name (e.g., User -> "user").

These schemas are used for validating incoming payloads in the API.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# ==============================
# USERS
# ==============================
class Address(BaseModel):
    line1: str
    line2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str

class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr
    phone: Optional[str] = None
    password: str = Field(..., description="Hashed password or temp plain for demo")
    address: Optional[Address] = None

# ==============================
# CATEGORIES
# ==============================
class Category(BaseModel):
    name: str
    icon: Optional[str] = None

# ==============================
# PRODUCTS
# ==============================
class Product(BaseModel):
    name: str
    category: str
    price: float = Field(..., ge=0)
    images: List[str] = []
    stock: int = Field(0, ge=0)
    description: Optional[str] = None
    ratings: float = Field(0, ge=0, le=5)
    discount_percent: Optional[float] = Field(0, ge=0, le=100)

# ==============================
# ORDERS
# ==============================
class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int = Field(..., ge=1)
    image: Optional[str] = None

class Order(BaseModel):
    user_id: str
    items: List[OrderItem]
    payment_method: str = Field(..., description="cod | card | wallet")
    total_amount: float = Field(..., ge=0)
    order_status: str = Field("pending")
    shipping_address: Address

# ==============================
# WISHLIST
# ==============================
class Wishlist(BaseModel):
    user_id: str
    product_id: str
