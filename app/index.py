from fastapi import FastAPI
from app.routes.app import dashboard
from starlette.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
import os


# Create the FastAPI application
app = FastAPI()

# Add middleware for database sessions
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# Include the user router in the application
app.include_router(dashboard, prefix='/app/v1')

# Define the CORS settings as constants
ALLOWED_ORIGINS = ["*"]
ALLOWED_METHODS = ["*"]
ALLOWED_HEADERS = ["*"]
ALLOW_CREDENTIALS = True

# Add CORS middleware to the application with the allowed origins, allow credentials,
# methods, and headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)