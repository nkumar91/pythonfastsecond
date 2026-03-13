
from app.api.middleware.security_middleware import limiter
from app.config.db import get_db
from app.schema.response import ApiResponse
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException,UploadFile,File,Form,Depends,status,Request
from sqlalchemy.orm import Session
from app.schema.users import UserCreate,UserRead as UserResponse
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



# @users.post("/signup/{id}")
# async def signup(id:int,user:UserCreate):
#     return {"message":user,id:id}

# @users.post("/file")
# async def upload_file(image: UploadFile = File(...)):
#     if not image.content_type.startswith("image/"):
#         raise HTTPException(400, "Only images allowed")
#     return {"file_size": len(image.file.read()), "file_name": image.filename}