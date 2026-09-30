import subprocess
import json

from core.models.relationship import Relationship



def query_table_relationships(
        query_observations,
        table_observations
):
    print("Inside")
    relationships = []


    # Map tables for quick lookup

    table_map = {}

    for table in table_observations:

        key = (
            table.data["database"]["name"],
            table.data["table"]["schema"],
            table.data["table"]["name"]
        )

        table_map[key] = table



    for query in query_observations:


        sql = query.data["query"].get("sql")

        database = (
            query.data["database"]
            .get("name")
        )


        if not sql or not database:
            continue


        tables = extract_tables_from_explain(
            database,
            sql
        )


        for schema, table_name in tables:


            table_obj = table_map.get(
                (
                    database,
                    schema,
                    table_name
                )
            )


            if not table_obj:
                continue



            relationships.append(

                Relationship(

                    source_entity_type="database_query",

                    source_entity_id=query.entity_id,


                    relationship_type="reads",


                    target_entity_type="database_table",

                    target_entity_id=table_obj.entity_id,


                    timestamp=query.timestamp

                )

            )

        print("outside")
    return relationships





def extract_tables_from_explain(
        database,
        sql
):
    print("In")
    tables = set()


    try:

        result = subprocess.run(

            [
                "sudo",
                "-u",
                "postgres",
                "psql",
                "-d",
                database,
                "-t",
                "-A",
                "-c",

                f"""
                EXPLAIN (FORMAT JSON)
                {sql}
                """
            ],

            capture_output=True,

            text=True,

            check=False

        )


        if not result.stdout.strip():
            return tables



        explain = json.loads(
            result.stdout
        )


        print(
            json.dumps(
                explain,
                indent=4
            )
        )
        plan = (
            explain[0]
            ["Plan"]
        )


        walk_plan(
            plan,
            tables
        )


    except Exception as e:

        print(
            "EXPLAIN failed:",
            e
        )

    print(tables)
    return tables




def walk_plan(
        node,
        tables,
        default_schema="public"
):

    if not node:
        return


    relation = node.get(
        "Relation Name"
    )


    schema = node.get(
        "Schema",
        default_schema
    )


    if relation:

        tables.add(
            (
                schema,
                relation
            )
        )


    for child in node.get(
        "Plans",
        []
    ):

        walk_plan(
            child,
            tables,
            default_schema
        )
