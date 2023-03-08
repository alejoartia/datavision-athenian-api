import io
import pandas as pd
from typing import Any, List, Dict, Optional
from app.analysis.dashboard_repository import DashboardRepository
from app.models.dashboard import Dashboard, FileCsv, QueriesAnalyzed, StatsId, TeamStats


class DashboardService:
    def __init__(self, dashboard_repository: DashboardRepository):
        self.dashboard_repository = dashboard_repository

    def upload_file(self, file: bytes) -> dict[str, str]:
        decoded_file: str = file.decode('utf-8')
        file_reader: pd.DataFrame = pd.read_csv(io.StringIO(decoded_file))
        file_csv = FileCsv()
        self.dashboard_repository.create_file_csv(file_csv)

        dashboards = [
            Dashboard(
                review_time=row.review_time,
                team=row.team,
                date=row.date,
                merge_time=row.merge_time,
                file_id=file_csv.id
            )
            for row in file_reader.itertuples()
        ]

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

    def get_review_stats(self) -> list[dict[str, Any]]:
        last_query_number: Optional[int] = self.dashboard_repository.get_last_query_number()

        if not last_query_number:
            return []

        dashboard_data: Optional[List[Dashboard]] = self.dashboard_repository.get_dashboard_data_by_query_number(
            last_query_number)

        if not dashboard_data:
            return []

        dashboard_info = [(d.id, d.review_time, d.team, d.date, d.merge_time) for d in dashboard_data]
        df = pd.DataFrame(dashboard_info, columns=['id', 'review_time', 'team', 'date', 'merge_time'])

        if df.empty:
            return []

        grouped_dashboard_data = df.groupby('team')
        mean_review_time = grouped_dashboard_data['review_time'].mean()
        median_review_time = grouped_dashboard_data['review_time'].median()
        mode_review_time = grouped_dashboard_data['review_time'].agg(pd.Series.mode).astype(float)
        mean_merge_time = grouped_dashboard_data['merge_time'].mean()
        median_merge_time = grouped_dashboard_data['merge_time'].median()
        mode_merge_time = grouped_dashboard_data['merge_time'].agg(pd.Series.mode).astype(float)

        review_stats = [{
            'name': team,
            'mean_review_time': mean_review_time[team],
            'median_review_time': median_review_time[team],
            'mode_review_time': mode_review_time[team].tolist(),
            'mean_merge_time': mean_merge_time[team],
            'median_merge_time': median_merge_time[team],
            'mode_merge_time': mode_merge_time[team].tolist()
        } for team in grouped_dashboard_data.groups]

        return review_stats

    def get_file_list(self) -> list[dict[str, Any]]:
        dashboard_list = self.dashboard_repository.get_files()

        if not dashboard_list:
            return []

        id_and_time_list = [(d.id, d.time_created) for d in dashboard_list]
        df = pd.DataFrame(id_and_time_list, columns=['_id', 'time_created'])

        if df.empty:
            return []

        user_stats_list = [{"id": d['_id'], "date": f"{d['time_created']: %Y-%m-%d %H:%M}"} for d in
                           df.to_dict('records')]
        return user_stats_list

    def save_stats(self) -> list[dict[str, Any]]:
        review_stats_data = self.get_review_stats()

        if not review_stats_data:
            return []

        df = pd.DataFrame(review_stats_data)

        max_query_number = self.dashboard_repository.get_max_query_number()

        if max_query_number is None:
            max_query_number = 1
        else:
            max_query_number += 1

        stats_id = StatsId(query_number=max_query_number)
        self.dashboard_repository.add_stats_id(stats_id)

        for row in df.itertuples():
            teamstats = TeamStats(
                name=row.name,
                mean_review_time=row.mean_review_time,
                median_review_time=row.median_review_time,
                mode_review_time=row.mode_review_time,
                mean_merge_time=row.mean_merge_time,
                median_merge_time=row.median_merge_time,
                mode_merge_time=row.mode_merge_time,
                stats_id=stats_id.query_number
            )
            self.dashboard_repository.add_team_stats(teamstats)

        return review_stats_data

    def get_analysis_data(self) -> List[Dict[str, str]]:
        analysis_data = self.dashboard_repository.get_analysis_data()

        if analysis_data is None:
            # If there is no analysis data, return an empty list
            return []

        stats = [
            {"query_number": row.query_number,
             "date": str(row.time_created.strftime('%Y-%m-%d %H:%M'))} for row in analysis_data
        ]
        return stats

    def get_team_stats_by_id(self, id: int) -> list[dict[str, Any]]:
        team_stats = self.dashboard_repository.get_team_stats_by_id(id)

        if not team_stats:
            # If there is no data for the specified ID, return an empty list
            return []

        data = [(d.id, d.name, d.mean_review_time, d.median_review_time, d.mode_review_time,
                 d.mean_merge_time, d.median_merge_time, d.mode_merge_time) for d in team_stats]

        stats_list = [{"id": d[0],
                       "name": d[1],
                       "mean_review_time": d[2],
                       "median_review_time": d[3],
                       "mode_review_time": d[4],
                       "mean_merge_time": d[5],
                       "median_merge_time": d[6],
                       "mode_merge_time": d[7]} for d in data]

        return stats_list
