from urllib.request import Request
from app.api.middleware.security_middleware import _rate_limit_exceeded_handle
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models
from fastapi.middleware.gzip import GZipMiddleware
from app.api.api import main_router
from app.config.db import Base, check_db_connection ,engine



app = FastAPI(
    title="My FastAPI Application",
    description="A sample FastAPI application for demonstration purposes.",
    version="1.0.0",
)

@app.on_event("startup")
def startup_event():
    if check_db_connection():  
        print("✅ Database connected successfully")
    else:
        print("❌ Database connection error")


# IN DEVELOPMENT, YOU CAN USE ["*"] TO ALLOW ALL ORIGINS FOR EASE OF TESTING
# orgins = [
#     "http://localhost:3000",
#     "http://localhost:8000",
#     "http://localhost:8080",
# ]
# IN DEVLOPMENT MODE, YOU CAN USE ["*"] TO ALLOW ALL ORIGINS FOR EASE OF TESTING
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
#     allow_credentials=True,
# )
# IN PRODUCTION, YOU SHOULD SPECIFY THE ORIGINS INSTEAD OF USING ["*"] TO ENHANCE SECURITY
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["Authorization", "Content-Type"],
# )



# RATE LIMITING SETUP
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# app.add_middleware(SlowAPIMiddleware)
_rate_limit_exceeded_handle(app) # HANDLE RATE LIMIT EXCEEDED ERRORS GLOBALLY

# @app.middleware("http")
# async def security_headers(request: Request, call_next):
#     response = await call_next(request)
#     response.headers["X-Frame-Options"] = "DENY"
#     return response

app.add_middleware(GZipMiddleware, minimum_size=1000)



Base.metadata.create_all(bind=engine)
app.include_router(main_router,prefix="/api")



@app.get("/")
async def get_firstTest():
    return {
        "message": "Hello, World!"
    }
