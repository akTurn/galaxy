import sqlite3
import json
from datetime import datetime

from core.models.observation import Observation


class SQLiteStore:

    def __init__(self, db_path: str = "galaxy.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()


    def _row_to_observation(self, row):
        source, entity_type, entity_id, timestamp, data = row

        return Observation(
            source=source,
            entity_type=entity_type,
            entity_id=entity_id,
            timestamp=datetime.fromisoformat(timestamp),
            data=json.loads(data),
        )


    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                entity_type TEXT,
                entity_id TEXT,
                timestamp TEXT,
                data TEXT
            )
        """)
        self.conn.commit()

    def save(self, observations: list[Observation]):
        rows = [
            (
                obs.source,
                obs.entity_type,
                obs.entity_id,
                obs.timestamp.isoformat(),
                json.dumps(obs.data),
            )
            for obs in observations
        ]

        self.conn.executemany(
            """
            INSERT INTO observations
                (source, entity_type, entity_id, timestamp, data)
            VALUES (?, ?, ?, ?, ?)
            """,
            rows,
        )
        self.conn.commit()

    def all(self):
        cursor = self.conn.execute(
            "SELECT source, entity_type, entity_id, timestamp, data FROM observations"
        )
        #return cursor.fetchall()
        return [
                    self._row_to_observation(row)
                    for row in cursor.fetchall()
                ]



    def count(self):
        cursor = self.conn.execute(
            "SELECT COUNT(*) FROM observations"
        )

        return cursor.fetchone()[0]


    def latest(self):
        cursor = self.conn.execute(
            """
            SELECT source, entity_type, entity_id, timestamp, data
            FROM observations
            ORDER BY id DESC
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_observation(row)


       # return cursor.fetchone()

#     Eventually ll change the method so it can filter:

# store.latest(
#     entity_type="host",
#     entity_id="localhost"
# )

    def find_by_entity(self, entity_type, entity_id):
        cursor = self.conn.execute(
            """
            SELECT source, entity_type, entity_id, timestamp, data
            FROM observations
            WHERE entity_type = ?
            AND entity_id = ?
            ORDER BY timestamp ASC
            """,
            (entity_type, entity_id),
        )

        #return cursor.fetchall()
        return [
            self._row_to_observation(row)
            for row in cursor.fetchall()
        ]

