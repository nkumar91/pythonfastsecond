from pydantic import ValidationError
from app.models.category import Category
from app.schema.category_schema import CategoryCreate
from app.schema.response import ApiResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


def create_category(db: Session, category: CategoryCreate):
    try:
        # Check if category with same name already exists
        existing_category = db.query(Category).filter(
            Category.cat_name == category.cat_name
        ).first()
        
        if existing_category:
            raise HTTPException(
                status_code=400,
                detail=ApiResponse(
                    success=False,
                    message="Category with this name already exists",
                    error="Duplicate category name"
                ).model_dump(mode="json", exclude_none=True)
            )
        
        # Create new category
        new_category = Category(
            cat_name=category.cat_name,
            cat_title=category.cat_title,
            cat_des=category.cat_des
        )
        
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=ApiResponse(
                success=False,
                message="Database Error",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )


def get_all_categories(db: Session):
    try:
        categories = db.query(Category).all()
        return categories
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                message="Database Error",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )


def get_category_by_id(db: Session, category_id: int):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        
        if not category:
            raise HTTPException(
                status_code=404,
                detail=ApiResponse(
                    success=False,
                    message="Category not found",
                    error=f"Category with ID {category_id} does not exist"
                ).model_dump(mode="json", exclude_none=True)
            )
        
        return category
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                message="Database Error",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )


def update_category(db: Session, category_id: int, category_data: CategoryCreate):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        
        if not category:
            raise HTTPException(
                status_code=404,
                detail=ApiResponse(
                    success=False,
                    message="Category not found",
                    error=f"Category with ID {category_id} does not exist"
                ).model_dump(mode="json", exclude_none=True)
            )
        
        # Update category fields
        category.cat_name = category_data.cat_name
        category.cat_title = category_data.cat_title
        category.cat_des = category_data.cat_des
        
        db.commit()
        db.refresh(category)
        return category
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=ApiResponse(
                success=False,
                message="Database Error",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )


def delete_category(db: Session, category_id: int):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        
        if not category:
            raise HTTPException(
                status_code=404,
                detail=ApiResponse(
                    success=False,
                    message="Category not found",
                    error=f"Category with ID {category_id} does not exist"
                ).model_dump(mode="json", exclude_none=True)
            )
        
        db.delete(category)
        db.commit()
        return {"id": category_id}
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                message="Database Error",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )
