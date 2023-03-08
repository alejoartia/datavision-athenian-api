import io
import pandas as pd
from app.analysis.dashboard_repository import DashboardRepository
from app.models.dashboard import Dashboard, FileCsv, QueriesAnalyzed


class DashboardService:
    def __init__(self, dashboard_repository: DashboardRepository):
        self.dashboard_repository = dashboard_repository

    def upload_file(self, file: bytes) -> dict[str, str]:
        decoded_file: str = file.decode('utf-8')
        file_reader: pd.DataFrame = pd.read_csv(io.StringIO(decoded_file))

        file_csv = FileCsv()
        self.dashboard_repository.create_file_csv(file_csv)

        dashboards = []
        for row in file_reader.itertuples():
            dashboard = Dashboard(
                review_time=row.review_time,
                team=row.team,
                date=row.date,
                merge_time=row.merge_time,
                file_id=file_csv.id
            )
            dashboards.append(dashboard)

        self.dashboard_repository.create_dashboards(dashboards)

        summary_stats: pd.DataFrame = file_reader.describe()
        return summary_stats.to_dict()

    def get_data(self, id: int) -> str:
        dashboard_data = self.dashboard_repository.get_dashboard_by_query_number(id)
        if dashboard_data is None:
            return "The query number does not exist"

        queries_analyzed = QueriesAnalyzed(
            query_number=id,
        )
        self.dashboard_repository.create_queries_analyzed(queries_analyzed)
        return 'The query has been saved'
