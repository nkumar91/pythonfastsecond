from datetime import datetime
from pydantic import BaseModel, field_serializer, field_validator
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
    cat_id: int | None
    @field_validator("cat_id")
    @classmethod
    def cat_id_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Category ID must be a positive integer")
        return v
    





class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    product_image_url: str | None
    cat_id: int | None
    created_at: datetime
    updated_at: datetime
    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")
    model_config = {"from_attributes": True}

class ProductWithCategoryResponse(BaseModel):
    id: int
    cat_name: str
    cat_title: str
    products: list[ProductResponse] | None = None
    model_config = {"from_attributes": True}