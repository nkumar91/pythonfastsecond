from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.config.db import get_db
from app.schema.category_schema import CategoryCreate, CategoryResponse
from app.schema.response import ApiResponse
from app.service.category_service import (
    create_category as service_create_category,
    get_all_categories,
    get_category_by_id,
    update_category as service_update_category,
    delete_category as service_delete_category
)
from sqlalchemy.orm import Session


category_router = APIRouter()


@category_router.post("/create_category", response_model=ApiResponse[CategoryResponse])
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    try:
        new_category = service_create_category(db, category_data)
        return JSONResponse(
            content=ApiResponse(
                success=True,
                message="Category created successfully",
                data=CategoryResponse.model_validate(new_category)
            ).model_dump(exclude_none=True)
        )
        
    except ValidationError as e:
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
            ).model_dump(mode="json", exclude_none=True)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                message="Failed to create category",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )


@category_router.get("/get_categories", response_model=ApiResponse[list[CategoryResponse]])
async def get_categories_endpoint(db: Session = Depends(get_db)):
    try:
        categories = get_all_categories(db)
        return JSONResponse(
            content=ApiResponse(
                success=True,
                message="Categories retrieved successfully",
                data=[CategoryResponse.model_validate(c) for c in categories]
            ).model_dump(exclude_none=True)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                message="Failed to retrieve categories",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )


@category_router.get("/get_category/{category_id}", response_model=ApiResponse[CategoryResponse])
async def get_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    try:
        category = get_category_by_id(db, category_id)
        
        return JSONResponse(
            content=ApiResponse(
                success=True,
                message="Category retrieved successfully",
                data=CategoryResponse.model_validate(category)
            ).model_dump(exclude_none=True)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                message="Failed to retrieve category",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )


@category_router.put("/update_category/{category_id}", response_model=ApiResponse[CategoryResponse])
async def update_category_endpoint(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    try:
        category = service_update_category(db, category_id, category_data)
        
        return JSONResponse(
            content=ApiResponse(
                success=True,
                message="Category updated successfully",
                data=CategoryResponse.model_validate(category)
            ).model_dump(exclude_none=True)
        )
        
    except ValidationError as e:
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
            ).model_dump(mode="json", exclude_none=True)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                message="Failed to update category",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )


@category_router.delete("/delete_category/{category_id}", response_model=ApiResponse[dict])
async def delete_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    try:
        result = service_delete_category(db, category_id)
        
        return JSONResponse(
            content=ApiResponse(
                success=True,
                message="Category deleted successfully",
                data=result
            ).model_dump(exclude_none=True)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                message="Failed to delete category",
                error=str(e)
            ).model_dump(mode="json", exclude_none=True)
        )
