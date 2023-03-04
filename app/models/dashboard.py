from typing import List, Optional
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, ARRAY, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Dashboard(Base):
    """
    Represents a dashboard object in the database.
    """
    __tablename__ = "Dashboard"
    id: int = Column(Integer, primary_key=True, index=True)
    review_time: int = Column(Integer)
    team: str = Column(String)
    date: Optional[Date] = Column(Date)
    merge_time: int = Column(Integer)

    file_id: int = Column(Integer, ForeignKey("file_csv.id"))

    file: "FileCsv" = relationship("FileCsv")


class FileCsv(Base):
    """
    Represents a CSV file object in the database.
    """
    __tablename__ = "FileCsv"
    id: int = Column(Integer, primary_key=True)
    time_created: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    time_updated: DateTime = Column(DateTime(timezone=True), onupdate=func.now())


class QueriesAnalyzed(Base):
    """
    Represents a queries analyzed object in the database.
    """
    __tablename__ = "QueriesAnalyzed"
    id: int = Column(Integer, primary_key=True)
    query_number: int = Column(Integer)
    time_created: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    time_updated: DateTime = Column(DateTime(timezone=True), onupdate=func.now())


class TeamStats(Base):
    """
    Represents a team stats object in the database.
    """
    __tablename__ = "team_stats"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    mean_review_time: float = Column(Float)
    median_review_time: float = Column(Float)
    mode_review_time: float = Column(Float)
    mean_merge_time: float = Column(Float)
    median_merge_time: float = Column(Float)
    mode_merge_time: float = Column(Float)
    date_created: DateTime = Column(DateTime(timezone=True), onupdate=func.now())

    stats_id: int = Column(Integer, ForeignKey("stats_id.id"))

    stat: "StatsId" = relationship("StatsId")


class StatsId(Base):
    """
    Represents a stats ID object in the database.
    """
    __tablename__ = "StatsId"
    id: int = Column(Integer, primary_key=True)
    query_number: int = Column(Integer)
    time_created: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    time_updated: DateTime = Column(DateTime(timezone=True), onupdate=func.now())