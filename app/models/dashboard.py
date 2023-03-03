from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, ARRAY

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

    file_id = Column(Integer, ForeignKey("FileCsv.id"))

    file = relationship("FileCsv")


class FileCsv(Base):
    __tablename__ = "FileCsv"
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class QueriesAnalyzed(Base):
    __tablename__ = "QueriesAnalyzed"
    id = Column(Integer, primary_key=True)
    query_number = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class TeamStats(Base):
    __tablename__ = "team_stats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mean_review_time = Column(Float)
    median_review_time = Column(Float)
    mode_review_time = Column(Float)
    mean_merge_time = Column(Float)
    median_merge_time = Column(Float)
    mode_merge_time = Column(Float)
    date_created = Column(DateTime(timezone=True), onupdate=func.now())

    stats_id = Column(Integer, ForeignKey("StatsId.id"))

    stat = relationship("StatsId")


class StatsId(Base):
    __tablename__ = "StatsId"
    id = Column(Integer, primary_key=True)
    query_number = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
