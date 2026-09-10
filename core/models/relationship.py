from dataclasses import dataclass
from datetime import datetime


@dataclass
class Relationship:
    source_entity_type: str
    source_entity_id: str

    relationship_type: str

    target_entity_type: str
    target_entity_id: str

    timestamp: datetime
