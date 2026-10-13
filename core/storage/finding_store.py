import json
import sqlite3
from datetime import datetime, timezone


class FindingStore:
    def __init__(self, db_path="galaxy.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    # def _create_table(self):
    #     self.conn.execute("""
    #         CREATE TABLE IF NOT EXISTS findings (
    #             finding_id TEXT PRIMARY KEY,
    #             rule_id TEXT NOT NULL,
    #             title TEXT NOT NULL,
    #             description TEXT NOT NULL,
    #             severity TEXT NOT NULL,
    #             affected_entities TEXT NOT NULL,
    #             evidence TEXT NOT NULL,
    #             first_seen TEXT NOT NULL,
    #             last_seen TEXT NOT NULL,
    #             occurrence_count INTEGER NOT NULL DEFAULT 1,
    #             status TEXT NOT NULL DEFAULT 'active',
    #             resolved_at TEXT
    #         )
    #     """)
    #     self.conn.commit()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS findings (
                finding_id TEXT PRIMARY KEY,
                rule_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT NOT NULL,
                affected_entities TEXT NOT NULL,
                evidence TEXT NOT NULL,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                occurrence_count INTEGER NOT NULL DEFAULT 1,
                status TEXT NOT NULL DEFAULT 'active',
                resolved_at TEXT
            )
        """)

        columns = {
            row[1]
            for row in self.conn.execute(
                "PRAGMA table_info(findings)"
            ).fetchall()
        }

        if "occurrence_count" not in columns:
            self.conn.execute("""
                ALTER TABLE findings
                ADD COLUMN occurrence_count INTEGER NOT NULL DEFAULT 1
            """)

        self.conn.commit()

    def save_evaluation(self, findings, evaluated_rule_ids):
        """
        Persist one successful evaluation of the specified rules.

        Findings returned by those rules become active.
        Previously active findings from those rules that are
        absent from this evaluation become resolved.
        """
        evaluated_rule_ids = set(evaluated_rule_ids)

        if not evaluated_rule_ids:
            return

        current_finding_ids = set()

        try:
            for finding in findings:
                if finding.rule_id not in evaluated_rule_ids:
                    raise ValueError(
                        f"Finding from unevaluated rule: {finding.rule_id}"
                    )

                current_finding_ids.add(finding.finding_id)

                self.conn.execute(
                    """
                    INSERT INTO findings (
                        finding_id, rule_id, title, description,
                        severity, affected_entities, evidence,
                        first_seen, last_seen,occurrence_count, status, resolved_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,1, 'active', NULL)
                    ON CONFLICT(finding_id) DO UPDATE SET
                        rule_id = excluded.rule_id,
                        title = excluded.title,
                        description = excluded.description,
                        severity = excluded.severity,
                        affected_entities = excluded.affected_entities,
                        evidence = excluded.evidence,
                        last_seen = excluded.last_seen,
                        occurrence_count = findings.occurrence_count + 1,
                        status = 'active',
                        resolved_at = NULL
                    """,
                    (
                        finding.finding_id,
                        finding.rule_id,
                        finding.title,
                        finding.description,
                        finding.severity,
                        json.dumps(finding.affected_entities),
                        json.dumps(finding.evidence),
                        finding.detected_at,
                        finding.detected_at,
                    ),
                )

            placeholders = ",".join("?" for _ in evaluated_rule_ids)

            rows = self.conn.execute(
                f"""
                SELECT finding_id
                FROM findings
                WHERE status = 'active'
                  AND rule_id IN ({placeholders})
                """,
                tuple(evaluated_rule_ids),
            ).fetchall()

            resolved_at = datetime.now(timezone.utc).isoformat()

            for (finding_id,) in rows:
                if finding_id not in current_finding_ids:
                    self.conn.execute(
                        """
                        UPDATE findings
                        SET status = 'resolved',
                            resolved_at = ?
                        WHERE finding_id = ?
                          AND status = 'active'
                        """,
                        (resolved_at, finding_id),
                    )

            self.conn.commit()

        except Exception:
            self.conn.rollback()
            raise

    def all_findings(self):
        rows = self.conn.execute(
            """
            SELECT
                finding_id, rule_id, title, description,
                severity, affected_entities, evidence,
                first_seen, last_seen,occurrence_count, status, resolved_at
            FROM findings
            ORDER BY first_seen DESC
            """
        ).fetchall()

        return [
            {
                "finding_id": row[0],
                "rule_id": row[1],
                "title": row[2],
                "description": row[3],
                "severity": row[4],
                "affected_entities": json.loads(row[5]),
                "evidence": json.loads(row[6]),
                "first_seen": row[7],
                "last_seen": row[8],
                "occurrence_count": row[9],
                "status": row[10],
                "resolved_at": row[11],
            }
            for row in rows
        ]

    def close(self):
        self.conn.close()
