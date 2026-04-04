from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.api.middleware.file_upload_middleware import validate_image
from app.config.db import get_db
from app.config.cloudinary import upload_to_cloudinary
from app.models.category import Category
from app.models.product_model import Product
from app.schema.product_schema import  ProductCreate, ProductCreate, ProductResponse, ProductWithCategoryResponse
from app.schema.response import ApiResponse
from app.service.product_service import create_product
from sqlalchemy.orm import Session
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 


product_router = APIRouter()


@product_router.post("/upload_product",response_model=ApiResponse[ProductResponse])
async def upload_file(
    name:str=Form(...),
    description:str=Form(...),
    price:float=Form(...),
    stock_quantity:int=Form(...),
    cat_id:int=Form(None),
    product_image: UploadFile = Depends(validate_image),
    db:Session=Depends(get_db)
    ):

    try:
        # Upload image to Cloudinary
        image_url = await upload_to_cloudinary(product_image)

        product_data = ProductCreate(
            name=name,
            description=description,
            price=price,
            cat_id=cat_id,
            stock_quantity=stock_quantity
        )
        new_product = create_product(db, product_data, image_url)
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
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                message="Upload failed",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )  


@product_router.get("/get_products",response_class=ORJSONResponse,response_model=ApiResponse[list[ProductResponse]]) 
async def get_products(db:Session=Depends(get_db)):
    try:
        products = db.query(Product).all()
        # result =  await db.execute(select(Product))
        # products = result.scalars().all()
        return ORJSONResponse(
            content=ApiResponse(
                success=True,
                message="Products retrieved successfully",
                data=[ProductResponse.model_validate(p) for p in products]
            ).model_dump(exclude_none=True)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                message="Failed to retrieve products",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )
   

@product_router.get("/get_product/{cat_id}",response_model=ApiResponse[ProductWithCategoryResponse])
async def get_product(cat_id:int, db:Session=Depends(get_db)):
    try:
        #category = db.query(Category).filter(Category.id == cat_id).first()
        results = (
            db.query(Product, Category)
            .join(Category, Product.cat_id == Category.id)
            .filter(Product.cat_id == cat_id)
            .all()
        )
        if not results:
            raise HTTPException(
                status_code=404,
                detail=ApiResponse(
                    success=False,
                    message="Category not found",
                    error=f"Category with ID {cat_id} does not exist"
                ).model_dump(mode="json", exclude_none=True)
            )
        _, category = results[0] 
        return JSONResponse(
            content=ApiResponse(
                success=True,
                message="Product retrieved successfully",
                data=ProductWithCategoryResponse(
                        id=category.id,
                        cat_name=category.cat_name,
                        cat_title=category.cat_title,
                        products=[ProductResponse.model_validate(product) for product, _ in results]
                    )
                
            ).model_dump(exclude_none=True)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                message="Failed to retrieve product",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )