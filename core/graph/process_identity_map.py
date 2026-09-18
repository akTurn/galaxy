class ProcessIdentityMap:

    def __init__(self, observations):

        self.by_pid = {} # dictionary to store pid for all observations

        for observation in observations:

            data = observation.data

            pid = data.get("pid")

            if pid is not None:
                self.by_pid[pid] = observation.entity_id

    def get(self, pid):# convenient way to look up an entity ID using a PID
        return self.by_pid.get(pid)


    # Suppose:

    # self.by_pid = {
    #     1234: "pid:1234@4567.89",
    #     5678: "pid:5678@5000.20"
    # }

    # Then:

    # identity_map.get(1234)

    # returns:

    # "pid:1234@4567.89"

    # In other words:

    # get(PID)
    # ↓
    # entity_id

    # So:

    # identity_map.get(1234)

    # means:

    # "Find the entity ID associated with PID 1234."
