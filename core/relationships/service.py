from core.models.relationship import Relationship


def service_relationships(
    service_observation,
    identity_map,
):

    """
    Given a 'service' Observation (with data['main_pid'] set by
    ServiceCollector), produce a relationship connecting the service
    to the stable process entity it currently manages.
 
    Service ---- runs_as/manages ----> Process
 
    If main_pid is 0 (no active main process) or the pid isn't in the
    current identity map (process not observed this cycle, or the
    lookup missed), we return no relationship rather than guessing.
    """
     
    relationships = []

    data = service_observation.data

    main_pid = data.get("main_pid")

    if not main_pid:
        return relationships

    process_entity_id = identity_map.get(main_pid)

    if process_entity_id is None:
        return relationships

    relationships.append(
        Relationship(
            source_entity_type="service",
            source_entity_id=service_observation.entity_id,

            relationship_type="manages",

            target_entity_type="process",
            target_entity_id=process_entity_id,

            timestamp=service_observation.timestamp,
        )
    )

    return relationships
