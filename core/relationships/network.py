from core.models.relationship import Relationship


def network_relationships(observation, identity_map):

    relationships = []

    # if observation.entity_type != "listening_port":
    #     return relationships

    
    # --------------------------------
    # Listening port
    # --------------------------------

    if observation.entity_type == "listening_port":

        pid = observation.data.get("pid")

        if pid is None:
            return relationships

        process_entity_id = identity_map.get(pid)

        if process_entity_id is None:
            return relationships

        relationships.append(
            Relationship(
                source_entity_type="process",
                source_entity_id=process_entity_id,
                relationship_type="listens_on",
                target_entity_type="listening_port",
                target_entity_id=observation.entity_id,
                timestamp=observation.timestamp,
            )
        )

        return relationships

    # --------------------------------
    # Network connection
    # --------------------------------

    if observation.entity_type == "network_connection":

        pid = observation.data.get("pid")

        if pid is None:
            return relationships

        process_entity_id = identity_map.get(pid)

        if process_entity_id is None:
            return relationships

        relationships.append(
            Relationship(
                source_entity_type="process",
                source_entity_id=process_entity_id,
                relationship_type="has_connection",
                target_entity_type="network_connection",
                target_entity_id=observation.entity_id,
                timestamp=observation.timestamp,
            )
        )

    return relationships
