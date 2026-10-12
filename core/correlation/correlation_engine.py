from core.correlation.finding import Finding


class CorrelationEngine:
    def __init__(self, store, graph, rules=None):
        self.store = store
        self.graph = graph
        self.rules = list(rules or [])

    def register_rule(self, rule):
        if any(
            existing.rule_id == rule.rule_id
            for existing in self.rules
        ):
            raise ValueError(
                f"Duplicate correlation rule: {rule.rule_id}"
            )

        self.rules.append(rule)

    def run_once(self):
        observations = self.store.all()
        findings = []

        for rule in self.rules:
            rule_findings = rule.evaluate(
                observations,
                self.graph,
            )

            if rule_findings is None:
                raise TypeError(
                    f"Rule {rule.rule_id} returned None; "
                    "expected a list of Finding objects"
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

        return findings
