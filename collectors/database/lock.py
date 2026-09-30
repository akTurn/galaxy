from datetime import datetime, timezone
import subprocess
import json

from core.models.observation import Observation


class DatabaseLockCollector:


    def collect(self,database_name):

        observations = []

        observations.extend(
            self._collect_postgresql(database_name)
        )

        return observations

    
    #  current DatabaseLockCollector only stores:

    
                # SELECT json_build_object(
                #     'pid', pid,
                #     'locktype', locktype,
                #     'mode', mode,
                #     'granted', granted,
                #     'relation', relation
                # )
                # FROM pg_locks;

    # "relation": relation

    # It does not store:

    # database name
    # schema
    # relation name
    # relkind

    # So the relationship function cannot determine that 32776 means expenses_pkey merely from the existing observations.


    
                # "sudo",
                # "-u",
                # "postgres",
                # "psql",
                #  "-d",
                # database_name,
                # "-t",
                # "-A",
                # "-c",
                # """         

                # SELECT json_build_object(
                #         'pid', l.pid,
                #         'locktype', l.locktype,
                #         'mode', l.mode,
                #         'granted', l.granted,
                #         'relation', l.relation,
                #         'schema', n.nspname,
                #         'relation_name', c.relname,
                #         'relkind', c.relkind
                #     )
                #     FROM pg_locks l
                #     LEFT JOIN pg_class c
                #         ON c.oid = l.relation
                #     LEFT JOIN pg_namespace n
                #         ON n.oid = c.relnamespace;

    def _collect_postgresql(self,database_name):

        observations = []


        result = subprocess.run(
            [
                "sudo",
                "-u",
                "postgres",
                "psql",
                 "-d",
                database_name,
                "-t",
                "-A",
                "-c",
                """         

                SELECT json_build_object(

                    'pid',
                    l.pid,

                    'locktype',
                    l.locktype,

                    'mode',
                    l.mode,

                    'granted',
                    l.granted,

                    'relation',
                    l.relation,

                    'schema',
                    n.nspname,

                    'relation_name',
                    c.relname,

                    'relkind',
                    c.relkind,

                    'query',
                    a.query

                )

                FROM pg_locks l

                LEFT JOIN pg_class c
                ON c.oid = l.relation

                LEFT JOIN pg_namespace n
                ON n.oid = c.relnamespace

                LEFT JOIN pg_stat_activity a
                ON l.pid = a.pid;
                """
            ],
            capture_output=True,
            text=True,
            check=False,
        )


        now = datetime.now(timezone.utc)


        for line in result.stdout.splitlines():

            if not line.strip():
                continue


            data = json.loads(line)


            pid = data["pid"]
            relation = data["relation"]


            observations.append(
                Observation(
                    source="database",
                    entity_type="database_lock",
                    #entity_id=f"postgresql:lock:{pid}:{relation}",
                    entity_id=(
                        f"postgresql:lock:"
                        f"{database_name}:"
                        f"{pid}:"
                        f"{data['locktype']}:"
                        f"{data['mode']}:"
                        f"{relation}"
                    ),
                    timestamp=now,
                    data={
                        "database":{
                            "engine":"postgresql",
                            "host":"localhost",
                            "name":database_name,
                        },
                        "lock":{
                            "pid":pid,
                            "locktype":data["locktype"],
                            "mode":data["mode"],
                            "granted":data["granted"],
                            "relation":relation,
                            "schema":data["schema"],
                            "relation_name":data["relation_name"],
                            "relkind":data["relkind"],
                            "query":data.get("query")
                        }
                    }
                )
            )


        return observations
