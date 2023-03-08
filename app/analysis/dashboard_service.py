import io
import pandas as pd
from typing import Any, List, Dict
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

    def get_review_stats(self) -> list[dict[str, Any]]:
        last_query_number = self.dashboard_repository.get_last_query_number()

        if last_query_number is None:
            return []

        dashboard_data: List[Dashboard] = self.dashboard_repository.get_dashboard_data_by_query_number(
            last_query_number)

        if dashboard_data is None:
            return []

        data = [(d.id, d.review_time, d.team, d.date, d.merge_time) for d in dashboard_data]
        df = pd.DataFrame(data, columns=['id', 'review_time', 'team', 'date', 'merge_time'])

        if df.empty:
            return []

        grouped_data = df.groupby("team")
        mean_review_time = grouped_data["review_time"].mean()
        median_review_time = grouped_data["review_time"].median()
        mode_review_time = grouped_data["review_time"].agg(pd.Series.mode).astype(float)

        mean_merge_time = grouped_data["merge_time"].mean()
        median_merge_time = grouped_data["merge_time"].median()
        mode_merge_time = grouped_data["merge_time"].agg(pd.Series.mode).astype(float)

        review_stats = []
        for team in grouped_data.groups:
            team_dict = {
                "name": team,
                "mean_review_time": mean_review_time[team],
                "median_review_time": median_review_time[team],
                "mode_review_time": mode_review_time[team].tolist(),
                "mean_merge_time": mean_merge_time[team],
                "median_merge_time": median_merge_time[team],
                "mode_merge_time": mode_merge_time[team].tolist(),
            }
            review_stats.append(team_dict)

        return review_stats

    def get_file_list(self) -> list[dict[str, Any]]:
        dashboard_data = self.dashboard_repository.get_files()

        if dashboard_data is None:
            return []

        data = [(d.id, d.time_created) for d in dashboard_data]
        df = pd.DataFrame(data, columns=['_id', 'time_created'])

        if df.empty:
            return []

        data_dict = df.to_dict('records')
        user_stats = [{"id": d['_id'], "date": d['time_created'].strftime('%Y-%m-%d %H:%M')} for d in data_dict]

        return user_stats

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

    def get_team_stats_by_id(self, id: int) -> List[Dict[str, Any]]:
        team_stats = self.dashboard_repository.get_team_stats_by_id(id)

        if team_stats is None:
            # If there is no data for the specified ID, return an empty list
            return []

        data = [(d.id,
                 d.name,
                 d.mean_review_time,
                 d.median_review_time,
                 d.mode_review_time,
                 d.mean_merge_time,
                 d.median_merge_time,
                 d.mode_merge_time) for d in team_stats]

        df = pd.DataFrame(data, columns=['id',
                                         'name',
                                         'mean_review_time',
                                         'median_review_time',
                                         'mode_review_time',
                                         'mean_merge_time',
                                         'median_merge_time',
                                         'mode_merge_time'])

        df_dict = df.to_dict(orient='records')

        # Create a new list of dictionaries with the desired keys
        stats_list = [{"id": d['id'],
                       "name": d['name'],
                       "mean_review_time": d['mean_review_time'],
                       "median_review_time": d['median_review_time'],
                       "mode_review_time": d['mode_review_time'],
                       "mean_merge_time": d['mean_merge_time'],
                       "median_merge_time": d['median_merge_time'],
                       "mode_merge_time": d['mode_merge_time']} for d in df_dict]

        return stats_list
