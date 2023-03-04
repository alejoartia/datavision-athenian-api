import io
import json
from typing import List, Dict, Any, Tuple

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import desc, func
from asyncio.log import logger

from fastapi import APIRouter, File
from fastapi_sqlalchemy import DBSessionMiddleware, db

from app.models.dashboard import (Dashboard, FileCsv, QueriesAnalyzed,
                                  TeamStats, StatsId)

load_dotenv(".env")

# Create an API router for the user endpoint
dashboard = APIRouter()


@dashboard.get('/')
async def home() -> dict[str, str] | tuple[dict[str, str], int]:
    """
    This is the home page, it just shows a message
    """
    try:
        return {"message": "Data-vision"}
    except Exception as e:
        # Log the exception for debugging purposes
        logger.exception("An exception occurred while handling the home page request")
        # Return an error response to the client
        return {"error": "An internal server error occurred"}, 500


@dashboard.post('/upload')
async def upload_file(file: bytes = File(...)) -> tuple[dict[str, str], int] | Any:
    """Handle CSV file uploads.

    Parse the uploaded CSV file, create a new `FileCsv` object and associate it with each row in the CSV,
    and return summary statistics for the uploaded data.

    Returns:
        A dictionary containing summary statistics for the uploaded data, or a tuple containing an error message
        and an HTTP status code if an error occurred during processing.
    """
    try:
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
    except Exception as e:
        # Log the exception for debugging purposes
        logger.exception("An exception occurred while handling the file upload request")
        # Return an error response to the client
        return {"error": "An internal server error occurred"}, 500


@dashboard.post('/analysis_file/{id}')
async def get_data(id: int):
    """
    Endpoint to retrieve dashboard data filtered by team, date, and id.

    Args:
        id: An integer representing the query number to filter by.

    Returns:
        A string indicating whether the query has been saved, or a dictionary containing an error message
        and an HTTP status code if an error occurred during processing.
    """
    try:
        dashboard_data = db.session.query(Dashboard).join(FileCsv).filter(
            QueriesAnalyzed.query_number == id
        )
        # Check if the query number exists in the database
        if dashboard_data is None:
            return {"error": "The query number does not exist"}, 404

        queries_analyzed = QueriesAnalyzed(
            query_number=id,
        )
        db.session.add(queries_analyzed)
        db.session.commit()

        return f'The query has been saved'
    except Exception as e:
        # Log the exception for debugging purposes
        logger.exception("An exception occurred while handling the analysis file request")
        # Return an error response to the client
        return {"error": "An internal server error occurred"}, 500


@dashboard.get('/review_stats')
async def review_stats() -> list[Any] | list[dict[str, Any]] | tuple[dict[str, str], int]:
    """
    Endpoint to retrieve review statistics for the most recent query.

    Returns a list of dictionaries, where each dictionary contains statistics for a single team,
    including the mean, median, and mode review and merge times.

    If no statistics are available (e.g., if no data has been analyzed yet), an empty list is returned.

    If an error occurs during processing, an error message and an HTTP status code of 500 is returned.
    """
    try:
        # Get the last query number from the database
        last_query_number = db.session.query(func.max(QueriesAnalyzed.query_number)).scalar()

        if last_query_number is None:
            # If there are no queries analyzed, return an empty list
            return []

        # Get the data from the database
        dashboard_data = db.session.query(Dashboard).join(FileCsv).filter(
            QueriesAnalyzed.query_number == last_query_number
        )

        if dashboard_data is None:
            # If there is no data for the last query number, return an empty list
            return []

        # Convert the data to a pandas DataFrame
        data = [(d.id, d.review_time, d.team, d.date, d.merge_time) for d in dashboard_data]
        df = pd.DataFrame(data, columns=['id', 'review_time', 'team', 'date', 'merge_time'])

        if df.empty:
            # If the DataFrame is empty, return an empty list
            return []

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

    except Exception as e:
        # If an error occurs, return a 500 status code and an error message
        return {"error": str(e)}, 500


@dashboard.get('/file_list')
async def get_user_stats() -> list[Any] | list[dict[str, Any]] | tuple[dict[str, str], int]:
    """
    Endpoint to retrieve a list of uploaded files with their creation timestamps.

    Returns a list of dictionaries, where each dictionary contains the file ID and creation timestamp
    for a single uploaded file.

    If no files have been uploaded yet, an empty list is returned.

    If an error occurs during processing, an error message and an HTTP status code of 500 is returned.
    """
    try:
        dashboard_data = db.session.query(FileCsv)

        if dashboard_data is None:
            # If there is no data, return an empty list
            return []

        data = [(d.id, d.time_created) for d in dashboard_data]
        df = pd.DataFrame(data, columns=['_id', 'time_created'])

        if df.empty:
            # If the DataFrame is empty, return an empty list
            return []

        data_dict = df.to_dict('records')

        user_stats = [{"id": d['_id'], "date": d['time_created'].strftime('%Y-%m-%d %H:%M')} for d in data_dict]

        return user_stats

    except Exception as e:
        # If an error occurs, return a 500 status code and an error message
        return {"error": str(e)}, 500


@dashboard.get('/save_analysis')
async def save_stats() -> list[Any] | list[dict[str, Any]] | tuple[dict[str, str], int] | tuple[dict[str, str], int]:
    """
    Endpoint to save review statistics into a JSON file and return the data.

    Calls the 'review_stats()' endpoint to get the statistics for the most recent query,
    saves the statistics to the database, and returns the statistics as a list of dictionaries.

    If no statistics are available (e.g., if no data has been analyzed yet), an empty list is returned.

    If an error occurs during processing, an error message and an HTTP status code of 500 is returned.
    """
    try:
        review_stats_data = await review_stats()  # Call review_stats() endpoint to get the data

        if not review_stats_data:
            # If there is no data, return an empty list
            return []

        df = pd.DataFrame(review_stats_data)

        max_query_number = db.session.query(func.max(StatsId.query_number)).scalar()

        if max_query_number is None:
            max_query_number = 1
        else:
            max_query_number += 1

        stats_id = StatsId(query_number=max_query_number)
        db.session.add(stats_id)
        db.session.commit()

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

        return review_stats_data  # Return the data as response

    except Exception as e:
        # If an error occurs, return a 500 status code and an error message
        return {"error": str(e)}, 500


@dashboard.get('/saved_analysis_list')
async def saved_analysis_list() -> list[Any] | list[dict[str, str | Any]] | tuple[dict[str, str], int]:
    """
    Endpoint to retrieve a list of saved analyses with their query numbers and creation timestamps.

    Returns a list of dictionaries, where each dictionary contains the query number and creation timestamp
    for a single saved analysis.

    If no analyses have been saved yet, an empty list is returned.

    If an error occurs during processing, an error message and an HTTP status code of 500 is returned.
    """
    try:
        analysis_data = db.session.query(StatsId).filter(StatsId.query_number.isnot(None))

        if analysis_data is None:
            # If there is no analysis data, return an empty list
            return []

        stats = [
            {"query_number": row.query_number,
             "date": str(row.time_created.strftime('%Y-%m-%d %H:%M'))} for row in analysis_data
        ]
        return stats

    except Exception as e:
        # If an error occurs, return a 500 status code and an error message
        return {"error": str(e)}, 500


@dashboard.post('/analysis/{id}')
async def saved_analysis_object(id: int) -> list[Any] | list[dict[str, Any]] | tuple[dict[str, str], int]:
    """
    Endpoint to retrieve a saved analysis by its ID.

    Returns a list of dictionaries, where each dictionary contains the statistics for a single team
    in the specified analysis.

    If no data is available for the specified ID, an empty list is returned.

    If an error occurs during processing, an error message and an HTTP status code of 500 is returned.
    """
    try:
        dashboard_data = db.session.query(TeamStats).filter(TeamStats.stats_id == id)

        if dashboard_data is None:
            # If there is no data for the specified ID, return an empty list
            return []

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

    except Exception as e:
        # If an error occurs, return a 500 status code and an error message
        return {"error": str(e)}, 500
