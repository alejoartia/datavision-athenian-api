from pydantic import BaseModel
from datetime import date
from typing import List


class Dashboard(BaseModel):
    review_time: int
    team: str
    date: date
    merge_time: int

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
    id: int
    name: str
    mean_review_time: float
    median_review_time: float
    mode_review_time: List[int]
    mean_merge_time: float
    median_merge_time: float
    mode_merge_time: List[int]
    date_created: date

    class Config:
        orm_mode = True
