from fastapi import FastAPI

# Create an API router for the user endpoint
dashboard = APIRouter()

@dashboard.get('/')
async def home():
    """
    This is the home page, it just shows a message
    """
    return "Welcome Data-vision"

