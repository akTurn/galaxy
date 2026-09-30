from core.models.relationship import Relationship


def table_column_relationships(
        table_observations,
        column_observations
):

    relationships = []


    table_map = {

        (
            table.data["database"]["name"],
            table.data["table"]["schema"],
            table.data["table"]["name"]

        ): table

        for table in table_observations
    }


    for column in column_observations:



        database = column.data["database"]["name"]

        schema = column.data["column"]["schema"]

        table_name = column.data["column"]["table"]


        table = table_map.get(
            (
                database,
                schema,
                table_name
            )
        )


        if not table:
            continue



        relationships.append(

            Relationship(

                source_entity_type="database_table",

                source_entity_id=table.entity_id,


                relationship_type="has_column",


                target_entity_type="database_column",

                target_entity_id=column.entity_id,


                timestamp=column.timestamp

            )

        )


    return relationships
