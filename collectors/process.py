# import psutil


# class ProcessCollector:

#     def collect(self):
#         processes = []

#         for process in psutil.process_iter(
#             ["pid", "name"]
#         ):
#             processes.append({
#                 "pid": process.info["pid"],
#                 "name": process.info["name"],
#             })

#         return processes

# import psutil
# from datetime import datetime, timezone
# from core.models.observation import Observation


# class ProcessCollector:

    # def collect(self) -> list[Observation]:
    #     observations = []

    #     for process in psutil.process_iter(["pid", "name"]):
    #         observations.append(
    #             Observation(
    #                 source="process",
    #                 entity_type="process",
    #                 entity_id=f"pid:{process.info['pid']}",
    #                 timestamp=datetime.now(timezone.utc),
    #                 data={
    #                     "pid": process.info["pid"],
    #                     "name": process.info["name"],
    #                 },
    #             )
    #         )

    #     return observations

    # def collect(self) -> list[Observation]:
    #     now = datetime.now(timezone.utc)
    #     observations = []

    #     for process in psutil.process_iter(
    #         ["pid", "name", "cpu_percent", "memory_percent"]
    #     ):
    #         observations.append(
    #             Observation(
    #                 source="process",
    #                 entity_type="process",
    #                 entity_id=f"pid:{process.info['pid']}",
    #                 timestamp=now,
    #                 data={
    #                     "pid": process.info["pid"],
    #                     "name": process.info["name"],
    #                     "cpu_percent": process.info["cpu_percent"],
    #                     "memory_percent": process.info["memory_percent"],
    #                 },
    #             )
    #         )

    #     return observations
    
import time
import psutil
from datetime import datetime, timezone
from core.models.observation import Observation
from core.models.process_identity import ProcessIdentity


class ProcessCollector:

    def collect(self) -> list[Observation]:
        # Step 1: prime cpu_percent for every process
        # (first call always returns 0.0 — this "starts the clock")
        for process in psutil.process_iter():
            try:
                process.cpu_percent(None)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Step 2: wait a moment so there's actual CPU activity to measure
        time.sleep(0.5)

        # Step 3: now take the real reading
        now = datetime.now(timezone.utc)
        observations = []

        for process in psutil.process_iter(
           # ["pid", "name", "cpu_percent", "memory_percent","status"]
           [
            "pid",
            "name",
            "cpu_percent",
            "memory_percent",
            "status",
            "username",
            "ppid",
            "exe",
            "cmdline",
            "create_time",
            ]
        ):

        ####/**************Why  added the try/except
            # This is important with process collection.

            # Processes can disappear while you're inspecting them.

            # For example:

            # process_iter()
            #      ↓
            # PID 4217 exists
            #      ↓
            # read information
            #      ↓
            # PID 4217 exits

            # Or you might not have permission to inspect a particular process.

            # So this:

            # except (psutil.NoSuchProcess, psutil.AccessDenied):
            #     continue

            # prevents one problematic process from killing the entire collection cycle.

            # That's especially important now that we're requesting more information.**************####

            try:
                info = process.info
                observations.append(
                    Observation(
                        source="process",
                        entity_type="process",
                        #entity_id=f"pid:{info['pid']}",
                        entity_id=ProcessIdentity.from_process(
                                info["pid"],
                                info["create_time"]
                            ),
                        timestamp=now,
                        data={
                            "pid": info["pid"],
                            "name": info["name"],
                            "cpu_percent": info["cpu_percent"],
                            "memory_percent": info["memory_percent"],
                            "status": info["status"],
                            "username": info["username"],
                            "parent_pid": info["ppid"],
                            "executable": info["exe"],
                            "command_line": info["cmdline"],
                            "create_time": info["create_time"],
                        },
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # A process can disappear or become inaccessible
                # between process_iter() and reading its information.
                continue

        return observations