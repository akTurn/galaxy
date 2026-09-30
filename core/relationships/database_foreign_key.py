from core.models.relationship import Relationship



def foreign_key_relationships(
        foreign_key_observations,
        table_observations
):

    relationships=[]


    table_map={}


    for table in table_observations:

        table_key = (
            table.data["database"]["name"],
            table.data["table"]["schema"],
            table.data["table"]["name"]
        )

        table_map[table_key]=table



    for fk in foreign_key_observations:


        data = fk.data["foreign_key"]


        database = fk.data["database"]["name"]


        source_key = (
            database,
            data["from_schema"],
            data["from_table"]
        )


        target_key = (
            database,
            data["to_schema"],
            data["to_table"]
        )



        source_table = table_map.get(source_key)

        target_table = table_map.get(target_key)



        if not source_table or not target_table:
            continue



        relationships.append(

            Relationship(

                source_entity_type="database_table",

                source_entity_id=source_table.entity_id,


                relationship_type="references",


                target_entity_type="database_table",

                target_entity_id=target_table.entity_id,


                timestamp=fk.timestamp

            )

        )


    return relationships
