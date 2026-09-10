from dataclasses import dataclass
from datetime import datetime


@dataclass
class Observation:
    source: str
    entity_type: str
    entity_id: str
    timestamp: datetime
    data: dict

