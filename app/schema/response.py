from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    model_config = {"exclude_none": True} 
    success: bool
    status_code: int = 200
    message: str
    data: Optional[T] = None
    error: Optional[T] = None
class ApiResponseProduct(BaseModel, Generic[T]):
    success: bool
   # status_code: int = 200
    message: str
    total_pages: int
    data: Optional[T] = None
    error: Optional[str] = None