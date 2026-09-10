from collectors.process import ProcessCollector
from core.graph.process_identity_map import ProcessIdentityMap
from core.relationships.process import process_relationships


collector = ProcessCollector()

observations = collector.collect()

identity_map = ProcessIdentityMap(
    observations
)

relationships = []

for observation in observations:

    relationships.extend(
        process_relationships(
            observation,
            identity_map
        )
    )

print("Processes:", len(observations))
print("Relationships:", len(relationships))

print()

for relationship in relationships[:10]:
    print(relationship)
