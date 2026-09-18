from collectors.process import ProcessCollector
from collectors.service import ServiceCollector
from core.graph.process_identity_map import ProcessIdentityMap
from core.relationships.service import service_relationships


process_observations = ProcessCollector().collect()
service_observations = ServiceCollector().collect()

identity_map = ProcessIdentityMap(process_observations)

relationships = []

for service in service_observations:

    relationships.extend(
        service_relationships(
            service,
            identity_map,
        )
    )


print("Services:", len(service_observations))
print("Processes:", len(process_observations))
print("Service relationships:", len(relationships))

print()

for relationship in relationships:

    print(
        relationship.source_entity_id,
        "->",
        relationship.relationship_type,
        "->",
        relationship.target_entity_id,
    )

for process in process_observations:
    if process.data.get("pid") == 23536:
        print(process)

