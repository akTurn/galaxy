from core.graph.machine_graph import MachineGraph


class CorrelationEngine:


    def __init__(self, store):

        self.store = store

        self.graph = MachineGraph(
            store
        )


    def analyze(self):

        events = []

        events.extend(
            self.detect_high_cpu()
        )

        return events




    def detect_high_cpu(self):

        events=[]


        processes = (
            self.store.latest_process_observations()
        )


        for process in processes:

            cpu = process.data.get(
                "cpu_percent",
                0
            )


            if cpu > 80:


                events.append({

                    "type":
                    "high_cpu_process",


                    "entity":
                    process.entity_id,


                    "evidence":
                    process.data

                })


        return events