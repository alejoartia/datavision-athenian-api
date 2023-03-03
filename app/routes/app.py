import json
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


@dashboard.post('/analysis_file/{id}')
async def get_data(id: int):
    """
    Endpoint to retrieve data filtered by team, date, and id
    """
    # Get the data from the database, filtered by team, date, and id
    dashboard_data = db.session.query(Dashboard).join(FileCsv).filter(FileCsv.id == id)
    # Convert the data to a pandas DataFrame
    data = [(d.id, d.review_time, d.team, d.date, d.merge_time) for d in dashboard_data]
    df = pd.DataFrame(data, columns=['id', 'review_time', 'team', 'date', 'merge_time'])
    print(df)
    return f'done!'


@dashboard.get('/review-stats')
async def get_user_stats() -> list:
    """
    Endpoint to retrieve data filtered by team and date
    """
    # Get the data from the database
    dashboard_data = db.session.query(Dashboard).join(FileCsv)
    # Convert the data to a pandas DataFrame
    data = [(d.id, d.review_time, d.team, d.date, d.merge_time) for d in dashboard_data]
    df = pd.DataFrame(data, columns=['id', 'review_time', 'team', 'date', 'merge_time'])
    # Group the data by team
    grouped_data = df.groupby("team")
    # Get the mean, median, and mode of the 'review_time' column for each team
    mean_review_time = grouped_data["review_time"].mean()
    median_review_time = grouped_data["review_time"].median()
    mode_review_time = grouped_data["review_time"].agg(pd.Series.mode)

    # Get the mean, median, and mode of the 'merge_time' column for each team
    mean_merge_time = grouped_data["merge_time"].mean()
    median_merge_time = grouped_data["merge_time"].median()
    mode_merge_time = grouped_data["merge_time"].agg(pd.Series.mode)
    # Create a list with the statistics for each team
    review_stats = []
    for team in grouped_data.groups:
        team_dict = {
            "name": team,
            "mean_review_time": mean_review_time[team],
            "median_review_time": median_review_time[team],
            "mode_review_time": mode_review_time[team].tolist(),
            "mean_merge_time": mean_merge_time[team],
            "median_merge_time": median_merge_time[team],
            "mode_merge_time": mode_merge_time[team].tolist(),
        }
        review_stats.append(team_dict)

    return review_stats


@dashboard.get('/filelist')
async def get_user_stats() -> list:
    """
    Endpoint to retrieve user stats
    """
    dashboard_data = db.session.query(FileCsv)
    data = [(d.id, d.time_created) for d in dashboard_data]
    df = pd.DataFrame(data, columns=['_id', 'time_created'])
    data_dict = df.to_dict('records')

    user_stats = [{"id": d['_id'], "date": d['time_created'].year} for d in data_dict]

    return user_stats
