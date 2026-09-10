from datetime import datetime, timezone

from core.models.relationship import Relationship
from core.storage.sqlite_store import SQLiteStore


store = SQLiteStore()

relationship = Relationship(
    source_entity_type="process",
    source_entity_id="pid:1539",

    relationship_type="parent_of",

    target_entity_type="process",
    target_entity_id="pid:39038",

    timestamp=datetime.now(timezone.utc),
)

store.save_relationships([relationship])

relationships = store.all_relationships()

print("Relationships:")

for item in relationships:
    print(item)
