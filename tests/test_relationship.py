from datetime import datetime, timezone

from core.models.observation import Observation
from core.relationships.process import process_relationships


observation = Observation(
    source="process",
    entity_type="process",
    entity_id="pid:39038",
    timestamp=datetime.now(timezone.utc),
    data={
        "pid": 39038,
        "name": "python",
        "parent_pid": 1539,
        "cpu_percent": 3.9,
        "memory_percent": 0.21,
    },
)


relationships = process_relationships(observation)

for relationship in relationships:
    print(relationship)
