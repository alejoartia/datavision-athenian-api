from fastapi import FastAPI
from app.routes.app import dashboard
from starlette.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
import os


app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# Include the user router in the application
app.include_router(dashboard, prefix='/app/v1')

# Allow all origins for CORS
origins = ["*"]

# Add CORS middleware to the application with the allowed origins, allow credentials,
# methods, and headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)