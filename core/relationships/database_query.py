from core.models.relationship import Relationship


def database_query_table_relationships(
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
