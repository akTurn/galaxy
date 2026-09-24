from datetime import datetime, timezone

from core.models.relationship import Relationship


def query_unix_socket_relationships(
        processes,
        sockets
):

    relationships = []

    now = datetime.now(timezone.utc)


    process_map = {
        p.data["pid"]: p
        for p in processes
    }


    for socket in sockets:

        pid = socket.data.get("process_pid")


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
