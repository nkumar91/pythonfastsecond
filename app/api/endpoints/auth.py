
from pydantic import ValidationError

from app.api.middleware.file_upload_middleware import validate_image
from app.api.middleware.security_middleware import limiter
from app.config.db import get_db
from app.models.product_model import Product
from app.schema.product_schema import ProductCreate, ProductResponse
from app.schema.response import ApiResponse
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException,UploadFile,File,Form,Depends,status,Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schema.users import UserCreate,UserRead as UserResponse
from typing import List
from app.service.product_service import create_product
#import pdb
users = APIRouter()

@users.get("/login")

async def login():
    return {"message":"Login Page"}


@users.post("/signup",response_model=ApiResponse[UserResponse])
@limiter.limit("10/minute")
async def signup(
    request: Request,
    name:str=Form(...),
    email:str=Form(...),
    password:str=Form(...),
    db:Session=Depends(get_db)
    ):
    try:
       # pdb.set_trace()
        user_data = UserCreate(name=name,email=email,password=password)
    except Exception as e:
        errors = []
        for err in e.errors():
            errors.append({
                "field": err["loc"][0],
                "message": err["msg"]
            })
        raise HTTPException(
            status_code=400, 
            detail=ApiResponse(
                success=False,
                message="Validation Error",
                error=errors
            ).model_dump(mode="json",exclude_none=True)
        )
        # return JSONResponse(
        #     status_code=status.HTTP_400_BAD_REQUEST,
        #     content=ApiResponse(
        #         success=False,
        #         message="Validation Error",
        #         error=errors
        #     ).model_dump()
        # )
    
    return JSONResponse(
            content=ApiResponse(
            success=True,
            message="User created successfully",
            data=UserResponse(
                id=1,
                name=user_data.name,
                email=user_data.email,
            )
        ).model_dump(mode="json",exclude_none=True)  # CONVERT TO JSON AND EXCLUDE NONE FIELDS
    )

@users.post("/upload_product",response_model=ApiResponse[ProductResponse])
async def upload_file(
    name:str=Form(...),
    description:str=Form(...),
    price:float=Form(...),
    stock_quantity:int=Form(...),
    #product_image: UploadFile = Depends(validate_image),
    db:Session=Depends(get_db)
    ):

    try:
        product_data = ProductCreate(
            name=name,
            description=description,
            price=price,
            stock_quantity=stock_quantity
        ) 
        new_product = create_product(db, product_data)
        return JSONResponse(
            content=ApiResponse(
                success=True,
                message="Product uploaded successfully",
                data=ProductResponse.model_validate(new_product)
            ).model_dump(exclude_none=True)  # EXCLUDE NONE FIELDS
        ) 

    except ValidationError as e:
                db.rollback()
                errors = []
                for err in e.errors():
                    errors.append({
                        "field": err["loc"][0],
                        "message": err["msg"]
                    })
                raise HTTPException(
                    status_code=400, 
                    detail=ApiResponse(
                        success=False,
                        message="Validation Error",
                        error=errors
                    ).model_dump(mode="json",exclude_none=True)
                )   
   

    #return {"file_size": len(product_image.file.read()), "file_name": product_image.filename}



# @users.post("/signup/{id}")
# async def signup(id:int,user:UserCreate):
#     return {"message":user,id:id}

# @users.post("/file")
# async def upload_file(image: UploadFile = File(...)):
    #     result = cloudinary.uploader.upload(
    #     file.file,
    #     public_id=file_name,
    #     folder="users"
    # )
#     if not image.content_type.startswith("image/"):
#         raise HTTPException(400, "Only images allowed")

#     return {"file_size": len(image.file.read()), "file_name": image.filename}