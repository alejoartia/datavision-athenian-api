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


@dashboard.get('/analysis')
async def get_data(team: str, date: str):
    """
    Endpoint to retrieve data filtered by team and date
    """
    # Get the data from the database
    dashboard_data = db.session.query(Dashboard). \
        join(FileCsv). \
        filter(Dashboard.team == team, Dashboard.date == date). \
        all()

    # Convert the data to a pandas DataFrame
    data = [(d.id, d.review_time, d.team, d.date, d.merge_time) for d in dashboard_data]
    df = pd.DataFrame(data, columns=['id', 'review_time', 'team', 'date', 'merge_time'])

    return f'done!'


@dashboard.get('/user-stats')
async def get_user_stats() -> list:
    """
    Endpoint to retrieve user stats
    """
    user_stats = [
        {
            "id": 1,
            "year": 2016,
            "userGain": 80000,
            "userLost": 823,
        },
        {
            "id": 2,
            "year": 2017,
            "userGain": 45677,
            "userLost": 345,
        },
        {
            "id": 3,
            "year": 2018,
            "userGain": 78888,
            "userLost": 555,
        },
        {
            "id": 4,
            "year": 2019,
            "userGain": 90000,
            "userLost": 4555,
        },
        {
            "id": 5,
            "year": 2020,
            "userGain": 4300,
            "userLost": 234,
        },
    ]

    return user_stats
