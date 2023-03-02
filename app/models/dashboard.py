from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Date

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Dashboard(Base):
    __tablename__ = "Dashboard"
    id = Column(Integer, primary_key=True, index=True)
    review_time = Column(Integer)
    team = Column(String)
    date = Column(Date)
    merge_time = Column(Integer)
