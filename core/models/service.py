from dataclasses import dataclass
from datetime import datetime


@dataclass
class Service:
    name: str
    state: str
    startup_type: str
    timestamp: datetime
