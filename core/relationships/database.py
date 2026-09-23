from core.models.relationship import Relationship


def database_session_relationships(
        database_observation,
        connection_observations
):

    relationships = []


    for connection in connection_observations:

        if (
            connection.data["database"]["engine"]
            ==
            database_observation.data["identity"]["engine"]
        ):

            relationships.append(
                Relationship(
                    source_entity_type="database",
                    source_entity_id=database_observation.entity_id,
                    relationship_type="has_session",
                    target_entity_type="database_connection",
                    target_entity_id=connection.entity_id,
                    timestamp=connection.timestamp,
                )
            )


    return relationships




def database_service_relationships(
        service_observations,
        database_observations
):

    relationships = []




    for service in service_observations:

        service_name = service.entity_id.lower()


        for database in database_observations:

            engine = database.data["identity"]["engine"]


            if engine in service_name:

                relationships.append(
                    Relationship(
                        source_entity_type="service",
                        source_entity_id=service.entity_id,
                        relationship_type="provides",
                        target_entity_type="database",
                        target_entity_id=database.entity_id,
                        timestamp=database.timestamp
                    )
                )


    return relationships




def database_process_relationships(
        process_observations,
        database_observations
):

    relationships=[]


    for process in process_observations:

        name = process.data["name"].lower()


        for database in database_observations:

            engine = database.data["identity"]["engine"]


            if engine in name:

                relationships.append(
                    Relationship(
                        source_entity_type="process",
                        source_entity_id=process.entity_id,
                        relationship_type="connects_to",
                        target_entity_type="database",
                        target_entity_id=database.entity_id,
                        timestamp=database.timestamp
                    )
                )


    return relationships

def application_database_relationships(
        application_relationships,
        process_database_relationships
):

    relationships=[]


    for app in application_relationships:

        if app.relationship_type != "runs":
            continue


        process_id = app.target_entity_id


        for db in process_database_relationships:

            if db.source_entity_id == process_id:

                relationships.append(
                    Relationship(
                        source_entity_type="application",
                        source_entity_id=app.source_entity_id,
                        relationship_type="uses",
                        target_entity_type="database",
                        target_entity_id=db.target_entity_id,
                        timestamp=db.timestamp
                    )
                )


    return relationships