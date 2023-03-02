from pydantic import BaseModel
from datetime import date


class Dashboard(BaseModel):
    review_time: int
    team: str
    date: date
    merge_time: int

    class Config:
        orm_mode = True
