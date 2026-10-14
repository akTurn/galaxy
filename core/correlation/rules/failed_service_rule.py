from core.correlation.correlation_rule import CorrelationRule
from core.correlation.finding import Finding


class FailedServiceRule(CorrelationRule):
    rule_id = "failed_service"
    description = "Detect system services in a failed state."

    def evaluate(self, observations, graph):
        findings = []

        for observation in observations:
            if observation.entity_type != "service":
                continue

            state = observation.data.get("state")

            if not isinstance(state, dict):
                continue

            active_state = state.get("active")

            if not isinstance(active_state, str):
                continue

            active_state = active_state.lower()

            if active_state != "failed":
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
                    title="Failed service detected",
                    description=(
                        f"Service {observation.entity_id} "
                        "is in a failed state."
                    ),
                    severity="high",
                    affected_entities=[entity],
                    evidence=[
                        {
                            "metric": "service_active_state",
                            "value": active_state,
                            "load_state": state.get("load"),
                            "sub_state": state.get("sub"),
                            "expected_state": "active",
                        }
                    ],
                )
            )

        return findings
