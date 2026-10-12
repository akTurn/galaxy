# from core.correlation.rules import (
#     HighCPUProcessRule
# )


# class CorrelationEngine:


#     def __init__(self, graph):

#         self.graph = graph


#         self.rules = [
#             HighCPUProcessRule()
#         ]



#     def analyze(
#         self,
#         observations
#     ):

#         findings = []


#         for rule in self.rules:

#             results = rule.evaluate(
#                 observations,
#                 self.graph
#             )

#             findings.extend(
#                 results
#             )


#         return findings

from core.correlation.rules import (
    HighCPUProcessRule
)

from core.correlation.finding_store import (
    FindingStore
)


class CorrelationEngine:

    def __init__(self, graph):

        self.graph = graph

        self.rules = [
            HighCPUProcessRule()
        ]

        self.finding_store = FindingStore()

    def analyze(self, observations):

        findings = []

        for rule in self.rules:

            results = rule.evaluate(
                observations,
                self.graph
            )

            for finding in results:

                stored_finding = (
                    self.finding_store.add(
                        finding
                    )
                )

                findings.append(
                    stored_finding
                )

        return findings