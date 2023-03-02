from fastapi import APIRouter, File
import pandas as pd
from dotenv import load_dotenv
from app.models.dashboard import Dashboard, FileCsv
from fastapi_sqlalchemy import DBSessionMiddleware, db
import io

load_dotenv(".env")

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
    decoded_file: str = file.decode('utf-8')
    file_reader: pd.DataFrame = pd.read_csv(io.StringIO(decoded_file))

    file_csv = FileCsv()
    db.session.add(file_csv)
    db.session.commit()

    for row in file_reader.itertuples():
        dashboard = Dashboard(
            review_time=row.review_time,
            team=row.team,
            date=row.date,
            merge_time=row.merge_time,
            file_id=file_csv.id
        )
        db.session.add(dashboard)
    db.session.commit()

    summary_stats: pd.DataFrame = file_reader.describe()
    return summary_stats.to_dict()
