from typing import List
from app.models.dashboard import Dashboard, FileCsv, QueriesAnalyzed, StatsId, TeamStats
from sqlalchemy import desc, func, not_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+psycopg2://postgres:password@db:5432/book_db"

db = create_async_engine(DATABASE_URL)


class DashboardRepository:

    @staticmethod
    async def create_file_csv_async(file_csv: FileCsv):
        async with AsyncSession(db) as session:
            async with session.begin():
                session.add(file_csv)

    @staticmethod
    async def create_file_csv(file_csv: FileCsv):
        async with AsyncSession(db) as session:
            async with session.begin():
                session.add(file_csv)

    @staticmethod
    async def create_dashboards(dashboards: list[Dashboard]):
        async with AsyncSession(db) as session:
            async with session.begin():
                session.add_all(dashboards)

    @staticmethod
    async def get_dashboard_by_query_number(id: int) -> Dashboard:
        async with AsyncSession(db) as session:
            query = await session.execute(
                select(Dashboard)
                .join(FileCsv)
                .filter(QueriesAnalyzed.query_number == id)
            )
            return query.scalar()

    @staticmethod
    async def create_queries_analyzed(queries_analyzed: QueriesAnalyzed):
        async with AsyncSession(db) as session:
            async with session.begin():
                session.add(queries_analyzed)

    @staticmethod
    async def get_last_query_number() -> int:
        async with AsyncSession(db) as session:
            return await session.execute(select(func.max(QueriesAnalyzed.query_number))).scalar()

    @staticmethod
    async def get_dashboard_data_by_query_number(last_query_number: int) -> List[Dashboard]:
        async with AsyncSession(db) as session:
            query = await session.execute(
                select(Dashboard)
                .join(FileCsv)
                .filter(QueriesAnalyzed.query_number == last_query_number)
            )
            return query.scalars().all()

    @staticmethod
    async def get_files() -> List[FileCsv]:
        async with AsyncSession(db) as session:
            query = await session.execute(select(FileCsv))
            return query.scalars().all()

    @staticmethod
    async def get_max_query_number() -> int:
        async with AsyncSession(db) as session:
            return await session.execute(select(func.max(StatsId.query_number))).scalar()

    @staticmethod
    async def add_stats_id(stats_id: StatsId) -> None:
        async with AsyncSession(db) as session:
            async with session.begin():
                session.add(stats_id)

    @staticmethod
    async def add_team_stats(teamstats: TeamStats) -> None:
        async with AsyncSession(db) as session:
            async with session.begin():
                session.add(teamstats)

    @staticmethod
    async def get_analysis_data() -> List[StatsId]:
        async with AsyncSession(db) as session:
            query = await session.execute(select(StatsId).filter(not_(StatsId.query_number.is_(None))))
            return query.scalars().all()

    @staticmethod
    async def get_team_stats_by_id(id: int) -> List[TeamStats]:
        async with AsyncSession(db) as session:
            query = await session.execute(select(TeamStats).filter(TeamStats.stats_id == id))
            return query.scalars().all()
