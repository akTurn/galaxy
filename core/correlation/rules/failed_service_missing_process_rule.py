
from core.correlation.correlation_rule import CorrelationRule
from core.correlation.finding import Finding


class FailedServiceMissingProcessRule(CorrelationRule):
    rule_id = "failed_service_missing_process"
    description = (
        "Detect failed services without a running main process."
    )

    def evaluate(self, observations, graph):
        findings = []

        services = [
            obs for obs in observations
            if obs.entity_type == "service"
        ]

        processes = [
            obs for obs in observations
            if obs.entity_type == "process"
        ]

        # Build the current PID -> process identity mapping.
        pid_to_process = {
            obs.data.get("pid"): obs.entity_id
            for obs in processes
            if obs.data.get("pid") is not None
        }

        for service in services:
            state = service.data.get("state", {})
            if not isinstance(state, dict):
                continue

            if state.get("active") != "failed":
                continue

            runtime = service.data.get("runtime", {})
            if not isinstance(runtime, dict):
                runtime = {}

            main_pid = runtime.get("main_pid")

            # Look for an existing service -> process graph edge.
            outgoing = graph.get_outgoing(
                "service",
                service.entity_id,
            )

            manages_edges = [
                edge for edge in outgoing
                if (
                    edge[2] == "manages"
                    and edge[3] == "process"
                )
            ]

            process_entity_id = (
                pid_to_process.get(main_pid)
                if main_pid
                else None
            )

            # A process is present only if its PID is in the
            # current process snapshot.
            process_missing = (
                not main_pid
                or process_entity_id is None
            )

            if not process_missing:
                continue

            if not main_pid:
                reason = "service has no active main PID"
            else:
                reason = (
                    f"main PID {main_pid} is absent from "
                    "the current process snapshot"
                )

            findings.append(
                Finding(
                    finding_id=(
                        f"{self.rule_id}:"
                        f"{service.entity_id}"
                    ),
                    rule_id=self.rule_id,
                    title=(
                        "Failed service has no running main process"
                    ),
                    description=(
                        f"Service {service.entity_id} is failed; "
                        f"{reason}."
                    ),
                    severity="high",
                    affected_entities=[
                        {
                            "entity_type": "service",
                            "entity_id": service.entity_id,
                        }
                    ],
                    evidence=[
                        {
                            "metric": "service_active_state",
                            "value": state.get("active"),
                            "expected": "active",
                        },
                        {
                            "metric": "service_main_pid",
                            "value": main_pid,
                            "expected": "PID present in current "
                            "process snapshot",
                        },
                        {
                            "metric": "managed_process_relationship",
                            "value": len(manages_edges),
                            "expected": (
                                "relationship to current process"
                            ),
                        },
                    ],
                )
            )

        return findings
