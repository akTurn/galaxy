
from core.correlation.correlation_rule import CorrelationRule
from core.correlation.finding import Finding


class HighProcessCountRule(CorrelationRule):
    rule_id = "high_process_count"
    description = "Detect a high number of observed processes."

    def __init__(self, threshold=300):
        self.threshold = threshold

    def evaluate(self, observations, graph):
        processes = [
            observation
            for observation in observations
            if observation.entity_type == "process"
        ]

        process_count = len(processes)

        if process_count <= self.threshold:
            return []

        return [
            Finding(
                finding_id=(
                    f"{self.rule_id}:"
                    f"{process_count}"
                ),
                rule_id=self.rule_id,
                title="High process count detected",
                description=(
                    f"Galaxy observed {process_count} processes, "
                    f"exceeding the configured threshold of "
                    f"{self.threshold}."
                ),
                severity="medium",
                affected_entities=[
                    {
                        "entity_type": "host",
                        "entity_id": "localhost",
                    }
                ],
                evidence=[
                    {
                        "metric": "process_count",
                        "value": process_count,
                        "threshold": self.threshold,
                        "comparison": "greater_than",
                    }
                ],
            )
        ]
