from core.correlation.rules import (
    HighCPUProcessRule
)


class CorrelationEngine:


    def __init__(self, graph):

        self.graph = graph


        self.rules = [
            HighCPUProcessRule()
        ]



    def analyze(
        self,
        observations
    ):

        findings = []


        for rule in self.rules:

            results = rule.evaluate(
                observations,
                self.graph
            )

            findings.extend(
                results
            )


        return findings