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

def query_process_relationships(
        query_observations,
        process_observations
):

    relationships = []

    # Create quick lookup by PID
    process_map = {
        str(process.data["pid"]): process
        for process in process_observations
    }


    for query in query_observations:

        pid = query.data["query"].get("pid")

        if not pid:
            continue


        process = process_map.get(str(pid))

        if not process:
            continue


        relationships.append(
            Relationship(
                source_entity_type="database_query",
                source_entity_id=query.entity_id,
                relationship_type="executed_by",
                target_entity_type="process",
                target_entity_id=process.entity_id,
                timestamp=query.timestamp,
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


def database_query_relationships(
        database_observation,
        query_observations
):
    relationships = []

    database_engine = database_observation.data["identity"]["engine"]

    for query in query_observations:

        query_engine = query.data["database"]["engine"]

        if database_engine != query_engine:
            continue

        relationships.append(
            Relationship(
                source_entity_type="database",
                source_entity_id=database_observation.entity_id,
                relationship_type="executes",
                target_entity_type="database_query",
                target_entity_id=query.entity_id,
                timestamp=query.timestamp,
            )
        )

    return relationships


def query_table_relationships(
        query_observations,
        table_observations
):

    relationships=[]


    for query in query_observations:

        sql = query.data["query"]["sql"]

        if not sql:
            continue


        sql = sql.lower()


        for table in table_observations:

            table_name = (
                table.data["table"]["name"]
                .lower()
            )


            if table_name in sql:

                relationships.append(
                    Relationship(
                        source_entity_type="database_query",
                        source_entity_id=query.entity_id,
                        relationship_type="accesses",
                        target_entity_type="database_table",
                        target_entity_id=table.entity_id,
                        timestamp=query.timestamp
                    )
                )


    return relationships




def database_lock_relationships(
        database_observation,
        lock_observations
):

    relationships = []

    engine = database_observation.data["identity"]["engine"]

    for lock in lock_observations:

        lock_engine = lock.data["database"]["engine"]

        if engine != lock_engine:
            continue


        relationships.append(
            Relationship(
                source_entity_type="database",
                source_entity_id=database_observation.entity_id,
                relationship_type="has_lock",
                target_entity_type="database_lock",
                target_entity_id=lock.entity_id,
                timestamp=lock.timestamp,
            )
        )


    return relationships



def database_table_relationships(
    instance_observations,
    table_observations
):
    relationships = []

    for instance in instance_observations:

        instance_database = instance.data["database"]

        for table in table_observations:

            table_database = table.data["database"]

            if (
                instance_database["engine"]
                != table_database["engine"]
            ):
                continue

            if (
                instance_database["name"]
                != table_database["name"]
            ):
                continue

            relationships.append(
                Relationship(
                    source_entity_type="database_instance",
                    source_entity_id=instance.entity_id,
                    relationship_type="contains",
                    target_entity_type="database_table",
                    target_entity_id=table.entity_id,
                    timestamp=table.timestamp,
                )
            )

    return relationships





def database_endpoint_relationships(
        database_observations,
        endpoint_observations
):

    relationships=[]


    for database in database_observations:

        engine = database.data["identity"]["engine"]


        for endpoint in endpoint_observations:

            endpoint_engine = (
                endpoint.data["database"]["engine"]
            )


            if engine != endpoint_engine:
                continue


            relationships.append(
                Relationship(
                    source_entity_type="database",
                    source_entity_id=database.entity_id,
                    relationship_type="listens_on",
                    target_entity_type="database_endpoint",
                    target_entity_id=endpoint.entity_id,
                    timestamp=endpoint.timestamp
                )
            )


    return relationships



def process_database_endpoint_relationships(
        process_observations,
        network_observations
):

    relationships=[]


    for process in process_observations:


        pid = process.data["pid"]


        for network in network_observations:


            if network.data.get("pid") != pid:
                continue


            relationships.append(
                Relationship(
                    source_entity_type="process",
                    source_entity_id=process.entity_id,
                    relationship_type="uses",
                    target_entity_type="network_connection",
                    target_entity_id=network.entity_id,
                    timestamp=network.timestamp
                )
            )


    return relationships


# def database_table_relationships(
#         database_observations,
#         table_observations
# ):

#     relationships=[]


#     for database in database_observations:

#         engine = database.data["identity"]["engine"]


#         for table in table_observations:

#             table_engine = (
#                 table.data["database"]["engine"]
#             )


#             if engine != table_engine:
#                 continue


#             relationships.append(
#                 Relationship(
#                     source_entity_type="database",
#                     source_entity_id=database.entity_id,
#                     relationship_type="contains",
#                     target_entity_type="database_table",
#                     target_entity_id=table.entity_id,
#                     timestamp=table.timestamp,
#                 )
#             )


#     return relationships