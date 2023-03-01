from fastapi import FastAPI
from app.routes.app import dashboard
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Include the user router in the application
app.include_router(dashboard, prefix='/api/v1')

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