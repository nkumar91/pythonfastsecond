from pydantic import BaseModel,EmailStr,Field,field_validator
from fastapi import Form
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email:EmailStr
    name:str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, examples=["password123"])
    @field_validator("password")
    @classmethod
    def password_must_have_number(cls, password):
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one number")
        return password.strip()
    @field_validator("name")
    @classmethod
    def name_must_be_alpha(cls, name):
        if not name.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters")
        return name.strip()
   
class UserLogin(BaseModel):
    email:EmailStr
    password:str = Field(...,min_length=6,examples=["password123"])

class UserRead(UserBase):
	"""Fields returned to clients (no password)"""
	id: int
	name:str
	email:str
	created_at: datetime = Field(default_factory=datetime.utcnow)
	model_config = {"from_attributes": True}