import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List

from config import ClaimsApiConfig


class ClaimsDBClient:
    def __init__(self, api_config: ClaimsApiConfig) -> None:
        self._database_path = api_config.claims_database_path
        self._table_name = api_config.claims_table_name

    @staticmethod
    def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    @contextmanager
    def _db_cursor(self):
        with sqlite3.connect(self._database_path) as db_conn:
            db_conn.row_factory = ClaimsDBClient.dict_factory
            try:
                cursor = db_conn.cursor()
                yield cursor
            finally:
                cursor.close()

    def get_claims(self, limit: int | None = None) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self._table_name}"
        if limit is not None:
            query += f" LIMIT {limit}"
        with self._db_cursor() as cur:
            query_results = cur.execute(query)
            query_results = query_results.fetchall()
        return query_results
