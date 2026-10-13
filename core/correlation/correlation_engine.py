
from core.correlation.finding import Finding

from core.storage.finding_store import FindingStore


class CorrelationEngine:

    def __init__(
        self,
        store,
        graph,
        rules,
        observation_mode="current",
        finding_store=None,
    ):
        self.store = store
        self.graph = graph
        self.rules = rules
        self.observation_mode = observation_mode

        self.finding_store = (
            finding_store
            if finding_store
            else FindingStore()
        )

    def register_rule(self, rule):
        if any(
            existing.rule_id == rule.rule_id
            for existing in self.rules
        ):
            raise ValueError(
                f"Duplicate correlation rule: {rule.rule_id}"
            )

        self.rules.append(rule)

    
    def _get_observations(self):
        if self.observation_mode == "history":
            return self.store.all()

        # Current-state observations for processes must use
        # the same snapshot as the current relationship graph.
        observations = self.store.latest_process_observations()

        # Get the latest observation for each identity for
        # these other entity types.
        entity_types = {
            "service",
            "host",
            "database",
            "database_health",
            "network_connection",
            "listening_port",
        }

        for entity_type in entity_types:
            observations.extend(
                self.store.latest_observations_by_entity_type(entity_type)
            )

        return observations


    def run_once(self):

        observations = self._get_observations()

        findings = []

        for rule in self.rules:

            rule_findings = rule.evaluate(
                observations,
                self.graph,
            )

            if not isinstance(rule_findings, list):
                raise TypeError(
                    f"Rule {rule.rule_id} must return "
                    "a list of Finding objects"
                )

            for finding in rule_findings:

                if not isinstance(finding, Finding):
                    raise TypeError(
                        f"Rule {rule.rule_id} returned "
                        "an invalid finding"
                    )

            findings.extend(rule_findings)


        if self.observation_mode == "current":

            self.finding_store.save_evaluation(
                findings,
                [
                    rule.rule_id
                    for rule in self.rules
                ],
            )


        return findings


    # def run_once(self):
    #     observations = self._get_observations()
    #     findings = []

    #     for rule in self.rules:
    #         rule_findings = rule.evaluate(
    #             observations,
    #             self.graph,
    #         )

    #         if not isinstance(rule_findings, list):
    #             raise TypeError(
    #                 f"Rule {rule.rule_id} must return "
    #                 "a list of Finding objects"
    #             )

    #         for finding in rule_findings:
    #             if not isinstance(finding, Finding):
    #                 raise TypeError(
    #                     f"Rule {rule.rule_id} returned "
    #                     "an invalid finding"
    #                 )

    #         findings.extend(rule_findings)

    #     return findings
