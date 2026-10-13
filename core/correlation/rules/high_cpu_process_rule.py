from core.correlation.correlation_rule import CorrelationRule
from core.correlation.finding import Finding


class HighCPUProcessRule(CorrelationRule):
    rule_id = "high_cpu_process"
    description = "Detect processes consuming unusually high CPU."

    def __init__(self, threshold=80.0):
        self.threshold = threshold

    def evaluate(self, observations, graph):
        findings = []

        for observation in observations:
            if observation.entity_type != "process":
                continue

            cpu_percent = observation.data.get("cpu_percent")

            if cpu_percent is None:
                continue

            try:
                cpu_percent = float(cpu_percent)
            except (TypeError, ValueError):
                continue

            if cpu_percent < self.threshold:
                continue

            entity = {
                "entity_type": observation.entity_type,
                "entity_id": observation.entity_id,
            }

            findings.append(
                Finding(
                    finding_id=(
                        f"{self.rule_id}:"
                        f"{observation.entity_id}"
                    ),
                    rule_id=self.rule_id,
                    title="High CPU usage detected",
                    description=(
                        f"Process {observation.entity_id} "
                        f"is using {cpu_percent:.1f}% CPU."
                    ),
                    severity=(
                        "critical"
                        if cpu_percent >= 95.0
                        else "high"
                    ),
                    affected_entities=[entity],
                    evidence=[
                        {
                            "metric": "cpu_percent",
                            "value": cpu_percent,
                            "threshold": self.threshold,
                        }
                    ],
                )
            )

        return findings
