from collectors.process import ProcessCollector
from collectors.network import NetworkCollector
from core.graph.process_identity_map import ProcessIdentityMap
from core.relationships.network import network_relationships


process_observations = ProcessCollector().collect()
network_observations = NetworkCollector().collect()

identity_map = ProcessIdentityMap(
    process_observations
)

relationships = []

for observation in network_observations:

    relationships.extend(
        network_relationships(
            observation,
            identity_map
        )
    )

print("Processes:", len(process_observations))



print(
    "Network observations:",
    len(network_observations)
)

print()
print("Listening ports:")

for observation in network_observations:

    if observation.entity_type == "listening_port":

        print(
            observation.entity_id,
            "PID =",
            observation.data.get("pid")
        )

print()
print("Network relationships:")

relationships = []

for observation in network_observations:

    relationships.extend(
        network_relationships(
            observation,
            identity_map
        )
    )

print("Relationships:", len(relationships))

# print(
#     "Network relationships:",
#     len(relationships)
# )

for relationship in relationships[:20]:

    print()

    print(relationship)
