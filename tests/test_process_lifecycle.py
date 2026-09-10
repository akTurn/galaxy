from core.graph.process_lifecycle import ProcessLifecycleTracker


class FakeObservation:

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.entity_type = "process"


tracker = ProcessLifecycleTracker()


# First collection
cycle_1 = [
    FakeObservation("pid:1@A"),
    FakeObservation("pid:2@B"),
    FakeObservation("pid:3@C"),
]

result = tracker.update(cycle_1)

print("Cycle 1")
print("Started:", result["started"])
print("Running:", result["running"])
print("Exited:", result["exited"])


# Second collection
cycle_2 = [
    FakeObservation("pid:1@A"),
    FakeObservation("pid:3@C"),
    FakeObservation("pid:4@D"),
]

result = tracker.update(cycle_2)

print()
print("Cycle 2")
print("Started:", result["started"])
print("Running:", result["running"])
print("Exited:", result["exited"])
