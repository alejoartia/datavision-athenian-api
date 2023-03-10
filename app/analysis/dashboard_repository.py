from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.analysis.dashboard_async_db import database, table_file_csv
from app.models.dashboard import Dashboard, FileCsv, QueriesAnalyzed, StatsId, TeamStats
from fastapi_sqlalchemy import db
from sqlalchemy import desc, func
from sqlalchemy.sql.expression import not_


class DashboardRepository:

    @staticmethod
    async def create_file_csv(file_csv: FileCsv):
        db.session.add(file_csv)
        db.session.commit()

    @staticmethod
    async def create_dashboards(dashboards: list[Dashboard]):
        db.session.add_all(dashboards)
        db.session.commit()

    @staticmethod
    async def get_dashboard_by_query_number(id: int) -> Dashboard:
        return db.session.query(Dashboard).join(FileCsv).filter(
            QueriesAnalyzed.query_number == id
        )

    @staticmethod
    async def create_queries_analyzed(queries_analyzed: QueriesAnalyzed):
        db.session.add(queries_analyzed)
        db.session.commit()

    @staticmethod
    async def get_last_query_number() -> int:
        return db.session.query(func.max(QueriesAnalyzed.query_number)).scalar()

    @staticmethod
    async def get_dashboard_data_by_query_number(last_query_number: int) -> Dashboard:
        return db.session.query(Dashboard).join(FileCsv).filter(
            QueriesAnalyzed.query_number == last_query_number
        ).all()

    @staticmethod
    async def get_files() -> List[FileCsv]:
        return db.session.query(FileCsv).all()

    @staticmethod
    async def get_max_query_number() -> int:
        return db.session.query(func.max(StatsId.query_number)).scalar()

    @staticmethod
    async def add_stats_id(stats_id: StatsId) -> None:
        db.session.add(stats_id)
        db.session.commit()

    @staticmethod
    async def add_team_stats(teamstats: TeamStats) -> None:
        db.session.add(teamstats)
        db.session.commit()

    @staticmethod
    async def get_analysis_data() -> List[StatsId]:
        return db.session.query(StatsId).filter(not_(StatsId.query_number.is_(None))).all()

    @staticmethod
    async def get_team_stats_by_id(id: int) -> List[TeamStats]:
        return db.session.query(TeamStats).filter(TeamStats.stats_id == id).all()
