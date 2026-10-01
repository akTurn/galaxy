from datetime import datetime, timezone
import uuid

from core.correlation.finding import Finding


class HighCPUProcessRule:


    def evaluate(
        self,
        observations,
        graph
    ):

        findings = []


        # --------------------
        # Find host
        # --------------------

        hosts = [
            obs
            for obs in observations
            if obs.entity_type == "host"
        ]


        for host in hosts:


            cpu = host.data.get(
                "cpu",
                0
            )


            if cpu < 90:
                continue



            # --------------------
            # Find processes
            # --------------------

            # processes = [
            #     obs
            #     for obs in observations
            #     if obs.entity_type == "process"
            # ]

            #/********************MachineGraph.get_current_neighbors() reads from SQLite,
            #  while observations contains the observations from the current collection.

            #So we'll use the graph to get the process entity IDs, 
            # then use those IDs to find the matching process observations.***********/

            neighbors = graph.get_current_neighbors(
                host.entity_id
            )

            process_ids = {
                neighbor["entity_id"]
                for neighbor in neighbors
                if (
                    neighbor["relationship"] == "runs"
                    and neighbor["direction"] == "out"
                )
            }

            processes = [
                obs
                for obs in observations
                if (
                    obs.entity_type == "process"
                    and obs.entity_id in process_ids
                )
            ]


            for process in processes:


                process_cpu = process.data.get(
                    "cpu_percent",
                    0
                )


                if process_cpu < 50:
                    continue



                findings.append(
                    Finding(

                        id=str(uuid.uuid4()),

                        rule_name=
                        "HighCPUProcessRule",

                        severity=
                        "warning",

                        title=
                        "High CPU process detected",

                        description=
                        (
                          f"Process "
                          f"{process.data.get('name')} "
                          f"is consuming "
                          f"{process_cpu}% CPU"
                        ),

                        # evidence={
                        #     "host_cpu": cpu,
                        #     "process_id":
                        #         process.entity_id,
                        #     "process_cpu":
                        #         process_cpu,
                        # },
                        evidence={

                            "host": host.entity_id,

                            "host_cpu": cpu,

                            "process": {
                                "id": process.entity_id,
                                "name": process.data.get("name"),
                                "cpu": process_cpu
                            },

                        },

                        timestamp=
                        datetime.now(
                            timezone.utc
                        )
                    )
                )


        return findings
