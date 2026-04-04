from pydantic import ValidationError
from app.models.product_model import Product
from app.schema.product_schema import ProductCreate
from app.schema.response import ApiResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


def create_product(db: Session, product: ProductCreate, image_url: str = None):
    try:
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            cat_id=product.cat_id,
            stock_quantity=product.stock_quantity,
            product_image_url=image_url
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except SQLAlchemyError as e:
                db.rollback()
                raise HTTPException(
                     status_code=400,
                     detail=ApiResponse(
                         success=False,
                         message="Db Error",
                         error=str(e)
                     ).model_dump(mode="json",exclude_none=True)
                 )