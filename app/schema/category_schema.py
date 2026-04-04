from datetime import datetime
from pydantic import BaseModel, field_validator, field_serializer


class CategoryCreate(BaseModel):
    cat_name: str

    @field_validator("cat_name")
    @classmethod
    def cat_name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Category name cannot be empty")
        return v

    cat_title: str

    @field_validator("cat_title")
    @classmethod
    def cat_title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Category title cannot be empty")
        return v

    cat_des: str | None = None


class CategoryResponse(BaseModel):
    id: int
    cat_name: str
    cat_title: str
    cat_des: str | None
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dt(self, value: datetime):
        return value.isoformat()

    class Config:
        from_attributes = True
