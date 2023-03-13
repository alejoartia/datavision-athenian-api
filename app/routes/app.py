from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
from asyncio.log import logger
from fastapi import APIRouter, File
from app.analysis.dashboard_service import DashboardService
from app.analysis.dashboard_repository import DashboardRepository
from app.analysis.dashboard_async_db import database

load_dotenv(".env")

# Create an API router for the user endpoint
dashboard = APIRouter()
dashboard_repository = DashboardRepository()
dashboard_service = DashboardService(dashboard_repository)



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
        return {"error": str(e)}, 500


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
        return await dashboard_service.upload_file(file=file)
    except Exception as e:
        # Log the exception for debugging purposes
        logger.exception("An exception occurred while handling the file upload request")
        # Return an error response to the client
        return {"error": str(e)}, 500


@dashboard.post('/analysis_file/{id}')
async def get_data(id: int):
    """
    Endpoint to retrieve dashboard data filtered by team, date, and id.
    Args: id: An integer representing the query number to filter by.
    Returns: A string indicating whether the query has been saved, or a dictionary containing an error message
    and an HTTP status code if an error occurred during processing.
    """
    try:
        return await dashboard_service.get_data(id=id)
    except Exception as e:
        # Log the exception for debugging purposes
        logger.exception("An exception occurred while handling the analysis file request")
        # Return an error response to the client
        return {"error": str(e)}, 500


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
        return await dashboard_service.get_review_stats()

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
        return await dashboard_service.get_file_list()

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
        return await dashboard_service.save_stats()

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
        stats = await dashboard_service.get_analysis_data()
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
        team_stats = await dashboard_service.get_team_stats_by_id(id)
        return team_stats

    except Exception as e:
        # If an error occurs, return a 500 status code and an error message
        return {"error": str(e)}, 500
