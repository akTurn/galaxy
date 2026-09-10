import sqlite3
import json
from datetime import datetime

from core.models.observation import Observation
from core.models.relationship import Relationship


class SQLiteStore:

    def __init__(self, db_path: str = "galaxy.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()
        self._create_relationships_table()


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
        #self.conn.commit()
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS lifecycle_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                entity_type TEXT,
                entity_id TEXT,
                timestamp TEXT
            )
        """)
        self.conn.commit()


    def save_lifecycle_events(self, events):

        rows = [
            (
                event.event_type,
                event.entity_type,
                event.entity_id,
                event.timestamp.isoformat(),
            )
            for event in events
        ]

        self.conn.executemany(
            """
            INSERT INTO lifecycle_events
                (event_type, entity_type, entity_id, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            rows,
        )

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


    # -------------------------
    # Relationships
    # -------------------------

    def _create_relationships_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_entity_type TEXT,
                source_entity_id TEXT,
                relationship_type TEXT,
                target_entity_type TEXT,
                target_entity_id TEXT,
                timestamp TEXT
            )
        """)

        self.conn.commit()

    def save_relationships(
        self,
        relationships: list[Relationship],
    ):
        rows = [
            (
                relationship.source_entity_type,
                relationship.source_entity_id,
                relationship.relationship_type,
                relationship.target_entity_type,
                relationship.target_entity_id,
                relationship.timestamp.isoformat(),
            )
            for relationship in relationships
        ]

        self.conn.executemany(
            """
            INSERT INTO relationships (
                source_entity_type,
                source_entity_id,
                relationship_type,
                target_entity_type,
                target_entity_id,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

        self.conn.commit()

    def all_relationships(self):
        cursor = self.conn.execute(
            """
            SELECT
                source_entity_type,
                source_entity_id,
                relationship_type,
                target_entity_type,
                target_entity_id,
                timestamp
            FROM relationships
            ORDER BY id ASC
            """
        )

        return cursor.fetchall()



    def get_children(self, parent_entity_id):
        cursor = self.conn.execute(
            """
            SELECT
                source_entity_type,
                source_entity_id,
                relationship_type,
                target_entity_type,
                target_entity_id,
                timestamp
            FROM relationships
            WHERE relationship_type = ?
            AND source_entity_id = ?
            ORDER BY id ASC
            """,
            ("parent_of", parent_entity_id),
        )

        return cursor.fetchall()


    def get_parent(self, child_entity_id):
        cursor = self.conn.execute(
            """
            SELECT
                source_entity_type,
                source_entity_id,
                relationship_type,
                target_entity_type,
                target_entity_id,
                timestamp
            FROM relationships
            WHERE relationship_type = ?
            AND target_entity_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            ("parent_of", child_entity_id),
        )

        return cursor.fetchone()

    def all_lifecycle_events(self):

        cursor = self.conn.execute(
            """
            SELECT
                event_type,
                entity_type,
                entity_id,
                timestamp
            FROM lifecycle_events
            ORDER BY timestamp ASC
            """
        )

        return cursor.fetchall()


    def get_recent_starts(self, limit=10):
        cursor = self.conn.execute(
            """
            SELECT
                event_type,
                entity_type,
                entity_id,
                timestamp
            FROM lifecycle_events
            WHERE event_type = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            ("process_started", limit),
        )

        return cursor.fetchall()


    def get_recent_exits(self, limit=10):
        cursor = self.conn.execute(
            """
            SELECT
                event_type,
                entity_type,
                entity_id,
                timestamp
            FROM lifecycle_events
            WHERE event_type = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            ("process_exited", limit),
        )

        return cursor.fetchall()


    def get_process_history(self, entity_id):
        cursor = self.conn.execute(
            """
            SELECT
                event_type,
                entity_type,
                entity_id,
                timestamp
            FROM lifecycle_events
            WHERE entity_id = ?
            ORDER BY timestamp ASC
            """,
            (entity_id,),
        )

        return cursor.fetchall()



