from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Finding:
    finding_id: str
    rule_id: str
    title: str
    description: str
    severity: str
    affected_entities: list[dict[str, str]] = field(
        default_factory=list
    )
    evidence: list[dict[str, Any]] = field(
        default_factory=list
    )
    detected_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    def __post_init__(self):
        allowed_severities = {
            "info",
            "low",
            "medium",
            "high",
            "critical",
        }

        if self.severity not in allowed_severities:
            raise ValueError(
                f"Invalid severity: {self.severity}"
            )

        if not self.finding_id:
            raise ValueError("finding_id cannot be empty")

        if not self.rule_id:
            raise ValueError("rule_id cannot be empty")
