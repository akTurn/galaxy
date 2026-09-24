import subprocess
from datetime import datetime, timezone

from core.models.observation import Observation


class UnixSocketCollector:

    def collect(self):

        now = datetime.now(timezone.utc)

        observations = []

        seen = set()


        result = subprocess.run(
            [
                "sudo",
                "lsof",
                "-nP",
                "-U"
            ],
            capture_output=True,
            text=True
        )


        for line in result.stdout.splitlines()[1:]:

            parts = line.split()

            if len(parts) < 8:
                continue


            command = parts[0]


            try:
                pid = int(parts[1])
            except ValueError:
                continue


            user = parts[2]


            # only unix socket rows
            if "unix" not in parts:
                continue


            # Find socket state
            state = None

            if "(LISTEN)" in parts:
                state = "LISTEN"

            elif "(CONNECTED)" in parts:
                state = "CONNECTED"


            # Find socket path
            socket_path = None

            for item in parts:

                if item.startswith("/"):
                    socket_path = item
                    break


            if not socket_path:
                continue


            # --------------------------
            # Deduplicate
            # --------------------------

            key = (
                pid,
                socket_path
            )


            if key in seen:
                continue


            seen.add(key)


            observations.append(
                Observation(
                    source="unix_socket",
                    entity_type="unix_socket",
                    entity_id=f"unix:{pid}:{socket_path}",
                    timestamp=now,
                    data={
                        "process_pid": pid,
                        "process_name": command,
                        "user": user,
                        "socket_path": socket_path,
                        "state": state
                    }
                )
            )


        return observations