from core.models.relationship import Relationship
from datetime import datetime, timezone


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


# def database_query_relationships(
#         database_observation,
#         query_observations
# ):
#     relationships = []

#     database_engine = database_observation.data["identity"]["engine"]

#     for query in query_observations:

#         query_engine = query.data["database"]["engine"]

#         if database_engine != query_engine:
#             continue

#         relationships.append(
#             Relationship(
#                 source_entity_type="database",
#                 source_entity_id=database_observation.entity_id,
#                 relationship_type="executes",
#                 target_entity_type="database_query",
#                 target_entity_id=query.entity_id,
#                 timestamp=query.timestamp,
#             )
#         )

#     return relationships

import re

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


            #if table_name in sql:
            

            pattern = r"\b" + table_name + r"\b"

            if re.search(pattern, sql):

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

def database_query_lock_relationships(
        query_observations,
        lock_observations
):

    relationships = []

    for query in query_observations:

        query_pid = (
            query
            .data
            .get("query", {})
            .get("pid")
        )

        if not query_pid:
            continue


        for lock in lock_observations:

            lock_pid = (
                lock
                .data
                .get("lock", {})
                .get("pid")
            )


            if str(query_pid) != str(lock_pid):
                continue


            relationships.append(
                Relationship(
                    source_entity_type="database_query",
                    source_entity_id=query.entity_id,
                    relationship_type="holds",
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



from datetime import datetime, timezone


def unix_socket_database_relationships(
        unix_socket_observations,
        database_observations
):

    relationships = []

    now=datetime.now(timezone.utc)


    for socket in unix_socket_observations:

        path = socket.data.get("socket_path")


        if ".s.PGSQL." not in path:
            continue


        for database in database_observations:


            if database.data["identity"]["engine"] == "postgresql":

                relationships.append(

                    Relationship(
                        source_entity_type="unix_socket",

                        source_entity_id=socket.entity_id,

                        relationship_type="belongs_to",

                        target_entity_type="database",

                        target_entity_id=database.entity_id,

                        timestamp=now
                    )

                )


    return relationships





def database_instance_relationships(
        database_observations,
        instance_observations
):

    relationships=[]

    now=datetime.now(timezone.utc)


    for db in database_observations:

        if db.entity_type!="database":
            continue


        for instance in instance_observations:


            if instance.data["database"]["engine"] == \
               db.data["identity"]["engine"]:


                relationships.append(

                    Relationship(

                        source_entity_type="database",

                        source_entity_id=db.entity_id,

                        relationship_type="contains",

                        target_entity_type="database_instance",

                        target_entity_id=instance.entity_id,

                        timestamp=now

                    )

                )


    return relationships


def process_database_connection_relationships(
        process_observations,
        connection_observations
):

    relationships=[]

    now=datetime.now(timezone.utc)


    processes = {
        str(p.data["pid"]): p
        for p in process_observations
    }


    for conn in connection_observations:

        if conn.entity_type != "database_connection":
            continue


        pid = conn.data["connection"].get("pid")


        if not pid:
            continue


        process = processes.get(str(pid))


        if not process:
            continue



        relationships.append(

            Relationship(

                source_entity_type="process",

                source_entity_id=process.entity_id,

                relationship_type="owns_connection",

                target_entity_type="database_connection",

                target_entity_id=conn.entity_id,

                timestamp=now

            )

        )


    return relationships


def database_connection_instance_relationships(
        connection_observations,
        instance_observations
):

    relationships = []

    now = datetime.now(timezone.utc)


    for connection in connection_observations:


        database_name = (
            connection
            .data
            .get("connection", {})
            .get("database")
        )


        if not database_name:
            continue



        for instance in instance_observations:


            instance_name = (
                instance
                .data
                .get("database", {})
                .get("name")
            )


            if database_name == instance_name:


                relationships.append(

                    Relationship(

                        source_entity_type="database_connection",

                        source_entity_id=connection.entity_id,

                        relationship_type="connected_to",

                        target_entity_type="database_instance",

                        target_entity_id=instance.entity_id,

                        timestamp=now

                    )

                )


    return relationships


def database_connection_query_relationships(
        connection_observations,
        query_observations
):

    relationships = []

    now = datetime.now(timezone.utc)


    for connection in connection_observations:


        connection_pid = (
            connection
            .data
            .get("connection", {})
            .get("pid")
        )


        if not connection_pid:
            continue



        for query in query_observations:


            query_pid = (
                query
                .data
                .get("query", {})
                .get("pid")
            )


            if connection_pid == query_pid:


                relationships.append(

                    Relationship(

                        source_entity_type="database_connection",

                        source_entity_id=connection.entity_id,

                        relationship_type="executes",

                        target_entity_type="database_query",

                        target_entity_id=query.entity_id,

                        timestamp=now

                    )
                )


    return relationships


def database_health_relationships(
        database_observations,
        health_observations
):

    relationships=[]


    for database in database_observations:

        engine = (
            database
            .data["identity"]["engine"]
        )


        for health in health_observations:

            health_engine = (
                health
                .data["database"]["engine"]
            )


            if engine != health_engine:
                continue


            relationships.append(

                Relationship(

                    source_entity_type="database",

                    source_entity_id=database.entity_id,

                    relationship_type="has_health",

                    target_entity_type="database_health",

                    target_entity_id=health.entity_id,

                    timestamp=health.timestamp

                )

            )


    return relationships

def database_index_relationships(
        table_observations,
        index_observations
):

    relationships = []


    table_map = {
        (
            table.data["table"]["schema"],
            table.data["table"]["name"]
        ): table
        for table in table_observations
    }


    for index in index_observations:

        index_data = index.data["index"]

        table = table_map.get(
            (
                index_data["schema"],
                index_data["table"]
            )
        )


        if not table:
            continue


        relationships.append(

            Relationship(

                source_entity_type="database_table",

                source_entity_id=table.entity_id,

                relationship_type="has_index",

                target_entity_type="database_index",

                target_entity_id=index.entity_id,

                timestamp=index.timestamp
            )
        )


    return relationships


def database_index_relationshipswithoutLookup(
        table_observations,
        index_observations
):

    relationships = []


    for table in table_observations:

        table_name = (
            table.data["table"]["name"]
        )

        schema = (
            table.data["table"]["schema"]
        )


        for index in index_observations:


            index_data = index.data["index"]


            # if (
            #     index_data["table"] == table_name
            #     and
            #     index_data["schema"] == schema
            # ):

            #add database matching also, because different databases can have the same table names
            if (
                index_data["table"] == table_name
                and
                index_data["schema"] == schema
                and
                index.data["database"]["name"] 
                    == table.data["database"]["name"]
            ):

                relationships.append(

                    Relationship(

                        source_entity_type="database_table",

                        source_entity_id=table.entity_id,

                        relationship_type="has_index",

                        target_entity_type="database_index",

                        target_entity_id=index.entity_id,

                        timestamp=index.timestamp

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