from core.correlation.correlation_rule import CorrelationRule
from core.correlation.finding import Finding


class ZombieProcessRule(CorrelationRule):
    rule_id = "zombie_process"
    description = "Detect processes in zombie state."

    def evaluate(self, observations, graph):
        findings = []

        for observation in observations:

            if observation.entity_type != "process":
                continue

            status = observation.data.get("status")

            if not isinstance(status, str):
                continue

            if status.lower() != "zombie":
                continue

            findings.append(
                Finding(
                    finding_id=(
                        f"{self.rule_id}:"
                        f"{observation.entity_id}"
                    ),
                    rule_id=self.rule_id,
                    title="Zombie process detected",
                    description=(
                        f"Process {observation.data.get('name', 'unknown')} "
                        f"({observation.entity_id}) is in zombie state."
                    ),
                    severity="medium",
                    affected_entities=[
                        {
                            "entity_type": "process",
                            "entity_id": observation.entity_id,
                        }
                    ],
                    evidence=[
                        {
                            "metric": "process_status",
                            "value": status,
                            "expected": "non-zombie",
                        }
                    ],
                )
            )

        return findings
