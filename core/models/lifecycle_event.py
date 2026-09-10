from dataclasses import dataclass
from datetime import datetime


@dataclass
class LifecycleEvent:

    event_type: str
    entity_type: str
    entity_id: str
    timestamp: datetime
