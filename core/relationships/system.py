from core.models.relationship import Relationship


def host_relationships(
    process_observations,
    service_observations,
):

    relationships = []


    # ----------------------------
    # HOST → PROCESS
    # ----------------------------

    for process in process_observations:

        relationships.append(

            Relationship(

                source_entity_type="host",
                source_entity_id="localhost",

                relationship_type="runs",

                target_entity_type="process",
                target_entity_id=process.entity_id,

                timestamp=process.timestamp,

            )
        )


    # ----------------------------
    # HOST → SERVICE
    # ----------------------------

    for service in service_observations:

        relationships.append(

            Relationship(

                source_entity_type="host",
                source_entity_id="localhost",

                relationship_type="provides",

                target_entity_type="service",
                target_entity_id=service.entity_id,

                timestamp=service.timestamp,

            )
        )


    return relationships