from core.models.relationship import Relationship


def process_relationships(observation, identity_map):
    #   Why identity_map?

    # Because relationship creation needs to answer:

    # What is the parent's full identity?

    # The identity map knows that.
    

    relationships = []

    data = observation.data

    pid = data.get("pid")
    parent_pid = data.get("parent_pid")

    if pid is None or parent_pid is None:
        return relationships

    parent_identity = identity_map.get(parent_pid)

    if parent_identity is None:
        return relationships

    relationships.append(
        Relationship(
            source_entity_type="process",
            source_entity_id=parent_identity,

            relationship_type="parent_of",

            target_entity_type="process",
            target_entity_id=observation.entity_id,

            timestamp=observation.timestamp,
        )
    )

    return relationships









# from core.models.relationship import Relationship


# def process_relationships(observation):

#     relationships = []

#     data = observation.data

#     parent_pid = data.get("parent_pid")
#     pid = data.get("pid")

#     if parent_pid and pid:

#         relationships.append(
#             Relationship(
#                 source_entity_type="process",
#                 source_entity_id=f"pid:{parent_pid}",

#                 relationship_type="parent_of",

#                 target_entity_type="process",
#                 target_entity_id=f"pid:{pid}",

#                 timestamp=observation.timestamp,
#             )
#         )

#     return relationships
