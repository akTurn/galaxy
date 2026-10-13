from core.correlation.correlation_rule import CorrelationRule
from core.correlation.finding import Finding


class HighMemoryProcessRule(CorrelationRule):
    rule_id = "high_memory_process"
    description = "Detect processes consuming unusually high memory."

    def __init__(self, threshold=80.0):
        self.threshold = threshold

    def evaluate(self, observations, graph):
        findings = []

        for observation in observations:
            if observation.entity_type != "process":
                continue

            memory_percent = observation.data.get("memory_percent")

            if memory_percent is None:
                continue

            try:
                memory_percent = float(memory_percent)
            except (TypeError, ValueError):
                continue

            if memory_percent < self.threshold:
                continue

            entity = {
                "entity_type": observation.entity_type,
                "entity_id": observation.entity_id,
            }

            findings.append(
                Finding(
                    finding_id=(
                        f"{self.rule_id}:{observation.entity_id}"
                    ),
                    rule_id=self.rule_id,
                    title="High memory usage detected",
                    description=(
                        f"Process {observation.entity_id} is using "
                        f"{memory_percent:.1f}% of system memory."
                    ),
                    severity=(
                        "critical"
                        if memory_percent >= 95.0
                        else "high"
                    ),
                    affected_entities=[entity],
                    evidence=[
                        {
                            "metric": "memory_percent",
                            "value": memory_percent,
                            "threshold": self.threshold,
                        }
                    ],
                )
            )

        return findings
