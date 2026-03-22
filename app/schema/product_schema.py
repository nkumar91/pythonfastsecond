from datetime import datetime

from pydantic import BaseModel, field_serializer, field_validator
from sqlalchemy import DateTime
from sqlalchemy import DateTime

class ProductCreate(BaseModel):
    name: str
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v
    description: str
    @field_validator("description")
    @classmethod
    def description_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Description cannot be empty")
        return v
    price: float
    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be a positive number")
        return v
    stock_quantity: int
    @field_validator("stock_quantity")
    @classmethod
    def stock_quantity_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Stock quantity cannot be negative")
        return v

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    created_at: datetime
    updated_at: datetime
    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")
    model_config = {"from_attributes": True}