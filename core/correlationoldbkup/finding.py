from dataclasses import dataclass
from datetime import datetime


@dataclass
class Finding:

    id: str

    rule_name: str

    severity: str

    title: str

    description: str

    evidence: dict

    status: str

    first_seen: datetime

    last_seen: datetime

    occurrences: int