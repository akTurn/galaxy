from core.models.relationship import Relationship


def log_relationships(
    log_observation,
    identity_map,
    service_map,
):

    relationships = []

    data = log_observation.data

    # -------------------------
    # Log → Process
    # -------------------------

    pid = data.get("pid")

    if pid is not None:

        process_entity_id = identity_map.get(pid)

        if process_entity_id is not None:

            relationships.append(
                Relationship(
                    source_entity_type="log",
                    source_entity_id=log_observation.entity_id,
                    relationship_type="generated_by",
                    target_entity_type="process",
                    target_entity_id=process_entity_id,
                    timestamp=log_observation.timestamp,
                )
            )

    # -------------------------
    # Log → Service
    # -------------------------

    service = data.get("service")

    if service is None:
        return relationships

    service_entity_id = (
        f"service:{service.removesuffix('.service')}"
    )

    if service_entity_id not in service_map:
        return relationships

    relationships.append(
        Relationship(
            source_entity_type="log",
            source_entity_id=log_observation.entity_id,
            relationship_type="associated_with",
            target_entity_type="service",
            target_entity_id=service_entity_id,
            timestamp=log_observation.timestamp,
        )
    )

    return relationships