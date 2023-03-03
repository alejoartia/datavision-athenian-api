import json
from typing import List, Dict, Any

from fastapi import APIRouter, File
import pandas as pd
from dotenv import load_dotenv
from app.models.dashboard import Dashboard, FileCsv, QueriesAnalyzed, TeamStats, StatsId
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import desc, func
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
    queries_analyzed = QueriesAnalyzed(
        query_number=id,
    )
    db.session.add(queries_analyzed)
    db.session.commit()

    print(id)
    return f'the query has been saved'


@dashboard.get('/review-stats')
async def review_stats() -> list:
    """
    Endpoint to retrieve data filtered by team and date

    """
    last_query_number = db.session.query(func.max(QueriesAnalyzed.query_number)).scalar()
    print(last_query_number)
    # Get the data from the database
    dashboard_data = db.session.query(Dashboard).join(FileCsv).filter(
        QueriesAnalyzed.query_number == last_query_number
    )
    # Convert the data to a pandas DataFrame
    data = [(d.id, d.review_time, d.team, d.date, d.merge_time) for d in dashboard_data]
    df = pd.DataFrame(data, columns=['id', 'review_time', 'team', 'date', 'merge_time'])
    # Group the data by team
    grouped_data = df.groupby("team")
    # Get the mean, median, and mode of the 'review_time' column for each team
    mean_review_time = grouped_data["review_time"].mean()
    median_review_time = grouped_data["review_time"].median()
    mode_review_time = grouped_data["review_time"].agg(pd.Series.mode).astype(float)

    # Get the mean, median, and mode of the 'merge_time' column for each team
    mean_merge_time = grouped_data["merge_time"].mean()
    median_merge_time = grouped_data["merge_time"].median()
    mode_merge_time = grouped_data["merge_time"].agg(pd.Series.mode).astype(float)
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

    user_stats = [{"id": d['_id'], "date": d['time_created'].strftime('%Y-%m-%d %H:%M')} for d in data_dict]

    return user_stats


@dashboard.get('/save_analysis')
async def save_stats() -> list:
    """
    Endpoint to save review_stats into a JSON file
    """
    review_stats_data = await review_stats()  # Call review_stats() endpoint to get the data
    df = pd.DataFrame(review_stats_data)

    max_query_number = db.session.query(func.max(StatsId.query_number)).scalar()
    if max_query_number is None:
        max_query_number = 1
    else:
        max_query_number += 1

    print(max_query_number)

    stats_id = StatsId(query_number=max_query_number)
    db.session.add(stats_id)
    db.session.commit()

    print(df)
    for row in df.itertuples():
        teamstats = TeamStats(
            name=row.name,
            mean_review_time=row.mean_review_time,
            median_review_time=row.median_review_time,
            mode_review_time=row.mode_review_time,
            mean_merge_time=row.mean_merge_time,
            median_merge_time=row.median_merge_time,
            mode_merge_time=row.mode_merge_time,
            stats_id=stats_id.query_number
        )
        db.session.add(teamstats)
    db.session.commit()

    print(review_stats_data)

    return review_stats_data  # Return the data as response


@dashboard.get('/saved_analysis_list')
async def saved_analysis_list() -> list[dict[str, Any]]:
    analysis_data = db.session.query(StatsId)
    data = [(d.id, d.time_created) for d in analysis_data]
    df = pd.DataFrame(data, columns=['_id', 'time_created'])
    data_dict = df.to_dict('records')

    stats = [{"id": d['_id'], "date": d['time_created'].strftime('%Y-%m-%d %H:%M')} for d in data_dict]

    return stats


@dashboard.get('/analysis/{id}')
async def saved_analysis_object() -> list[dict[str, Any]]:
    """
    Endpoint to save review_stats into a JSON file
    """

    dashboard_data = db.session.query(TeamStats)

    data = [(d.id,
             d.name,
             d.mean_review_time,
             d.median_review_time,
             d.mode_review_time,
             d.mean_merge_time,
             d.median_merge_time,
             d.mode_merge_time) for d in dashboard_data]

    df = pd.DataFrame(data, columns=['id',
                                     'name',
                                     'mean_review_time',
                                     'median_review_time',
                                     'mode_review_time',
                                     'mean_merge_time',
                                     'median_merge_time',
                                     'mode_merge_time'])

    df_dict = df.to_dict(orient='records')

    # Create a new list of dictionaries with the desired keys
    stats_list = [{"id": d['id'],
                   "name": d['name'],
                   "mean_review_time": d['mean_review_time'],
                   "median_review_time": d['median_review_time'],
                   "mode_review_time": d['mode_review_time'],
                   "mean_merge_time": d['mean_merge_time'],
                   "median_merge_time": d['median_merge_time'],
                   "mode_merge_time": d['mode_merge_time']} for d in df_dict]

    return stats_list
