from core.models.relationship import Relationship
from datetime import datetime, timezone


def query_unix_socket_relationships(
        process_observations,
        unix_socket_observations
):

    relationships = []

    now = datetime.now(timezone.utc)


    # create lookup
    process_map = {
        p.data["pid"]: p
        for p in process_observations
    }


    for socket in unix_socket_observations:

        pid = socket.data["process_pid"]


        process = process_map.get(pid)


        if not process:
            continue


        relationships.append(
            Relationship(
                source_entity_type="process",
                source_entity_id=process.entity_id,
                relationship_type="connected_through",
                target_entity_type="unix_socket",
                target_entity_id=socket.entity_id,
                timestamp=now
            )
        )


    return relationships