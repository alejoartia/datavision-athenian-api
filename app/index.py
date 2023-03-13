from fastapi import FastAPI
from app.routes.app import dashboard
from starlette.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import os
from app.analysis.dashboard_async_db import connect, disconnect

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


# Define a function to generate the OpenAPI specification
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Data-Vision Athenian API by Alejandro Cordoba",
        version="1.0.0",
        description="This is a RESTful API server that enables users to upload CSV data, view summary statictics, "
                    "create visualization. Is designed to be scalable and high-performing. It provides a reange of "
                    "visualisation options as charts, bar charts, and scatter plots. Topics Resources",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Define a route to return the OpenAPI specification
@app.get("/openapi.json")
async def get_openapi_spec():
    return JSONResponse(content=custom_openapi())


# for async
@app.on_event("startup")
async def startup():
    await connect()


@app.on_event("shutdown")
async def shutdown():
    await disconnect()
