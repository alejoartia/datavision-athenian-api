from datetime import date
from typing import Annotated
from pydantic import BaseModel, validator, root_validator


class Dashboard(BaseModel):
    review_time: Annotated[int, "Number of seconds"]
    team_name: str
    review_date: date
    merge_time: Annotated[int, "Number of seconds"]

    class Config:
        orm_mode = True


class FileCsv(BaseModel):
    name: str

    class Config:
        orm_mode = True


class QueriesAnalyzed(BaseModel):
    query_number: int

    class Config:
        orm_mode = True


class TeamStats(BaseModel):
    team_id: int
    team_name: str
    mean_review_time: float
    median_review_time: float
    mode_review_time: float
    mean_merge_time: float
    median_merge_time: float
    mode_merge_time: float
    created_date: date

    class Config:
        orm_mode = True


class StatsId(BaseModel):
    query_number: int

    class Config:
        orm_mode = True
