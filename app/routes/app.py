from fastapi import APIRouter, File
import pandas as pd
import io

# Create an API router for the user endpoint
dashboard = APIRouter()


@dashboard.get('/')
async def home() -> dict:
    """
    This is the home page, it just shows a message
    """
    return {"message": "Data-vision"}


@dashboard.post('/upload')
async def upload_file(file: bytes = File(...)) -> dict:
    """
    This method allows to upload files
    """
    decoded_file: str = file.decode('utf-8')
    file_reader: pd.DataFrame = pd.read_csv(io.StringIO(decoded_file))
    summary_stats: pd.DataFrame = file_reader.describe()
    return summary_stats.to_dict()
