from app.models.dashboard import Dashboard, FileCsv, QueriesAnalyzed
from fastapi_sqlalchemy import db


class DashboardRepository:
    @staticmethod
    def create_file_csv(file_csv: FileCsv):
        db.session.add(file_csv)
        db.session.commit()

    @staticmethod
    def create_dashboards(dashboards: list[Dashboard]):
        db.session.add_all(dashboards)
        db.session.commit()

    @staticmethod
    def get_dashboard_by_query_number(id: int) -> Dashboard:
        return db.session.query(Dashboard).join(FileCsv).filter(
            QueriesAnalyzed.query_number == id
        ).first()

    @staticmethod
    def create_queries_analyzed(queries_analyzed: QueriesAnalyzed):
        db.session.add(queries_analyzed)
        db.session.commit()
