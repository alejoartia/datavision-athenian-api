from datetime import date
from typing import Annotated
from pydantic import BaseModel, validator, root_validator


class Dashboard(BaseModel):
    review_time: Annotated[int, "Number of seconds"]
    team_name: str
    review_date: date
    merge_time: Annotated[int, "Number of seconds"]

    # This is because in a normal distribution of review times,
    # the mean is typically less than the median. If the mean is greater than or equal to the median,
    # it suggests that the distribution is skewed
    @validator("review_time", "merge_time")
    def check_time_range(self, v):
        if v < 0 or v > 86400:
            raise ValueError("Time must be between 0 and 86400 seconds")
        return v

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

    # This is because in a normal distribution of review times,
    # the mean is typically less than the median. If the mean is greater than or equal to the median,
    # it suggests that the distribution is skewed
    @root_validator
    def check_time_order(self, values):
        if values.get("mean_review_time") >= values.get("median_review_time"):
            raise ValueError("Mean review time must be less than median review time")
        return values

    class Config:
        orm_mode = True


class StatsId(BaseModel):
    query_number: int

    class Config:
        orm_mode = True
