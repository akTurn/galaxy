class ProcessIdentityMap:

    def __init__(self, observations):

        self.by_pid = {}

        for observation in observations:

            data = observation.data

            pid = data.get("pid")

            if pid is not None:
                self.by_pid[pid] = observation.entity_id

    def get(self, pid):
        return self.by_pid.get(pid)
