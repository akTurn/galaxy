from core.models.relationship import Relationship


def host_relationships(observation):

    

    return Relationship(
        source_entity_type="host",
        source_entity_id="localhost",

        relationship_type="hosts",

        target_entity_type="process",
        target_entity_id=observation.entity_id,

        timestamp=observation.timestamp,
    )