from pydantic import BaseModel
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    image_url: str
    stock_quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str
    stock_quantity: int