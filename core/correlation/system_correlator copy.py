from core.correlation.correlation_result import (
    CorrelationResult,
)
from core.correlation.relationship_weights import relationship_weight


class SystemCorrelator:


    def __init__(
        self,
        graph,
    ):
        self.graph = graph



    def correlate(
        self,
        findings,
    ):

        results = []


        for index, first in enumerate(findings):

            for second in findings[index + 1:]:


                result = self._compare(
                    first,
                    second,
                )


                if result:
                    results.append(result)


        return results



    def _compare(
        self,
        first,
        second,
    ):

        for entity_a in first.affected_entities:

            for entity_b in second.affected_entities:


                path = self.graph.shortest_path(
                    entity_a["entity_type"],
                    entity_a["entity_id"],
                    entity_b["entity_type"],
                    entity_b["entity_id"],
                )


                # if path:

                #     return CorrelationResult(

                #         finding_ids=[
                #             first.finding_id,
                #             second.finding_id,
                #         ],

                #         reasons=[
                #             "Graph relationship exists"
                #         ],

                #         confidence=0.8,
                #     )

                if path and self._time_related(first, second):

                        return CorrelationResult(
                            finding_ids=[
                                first.finding_id,
                                second.finding_id,
                            ],

                            reasons=[
                                "Graph relationship exists",
                                "Findings occurred within time window",
                            ],

                            #confidence=0.85,
                            confidence = self._calculate_confidence(path),

                            detected_window={
                                "first": first.detected_at,
                                "second": second.detected_at,
                            }
                        )


        return None


    def _calculate_confidence(self, path):

        score = 1.0

        for edge in path:
            relationship = edge.get(
                "relationship"
            )

            score *= relationship_weight(
                relationship
            )

        return round(score, 2)

    def _time_related(
        self,
        first,
        second,
        window_seconds=300,
    ):

        from datetime import datetime


        first_time = datetime.fromisoformat(
            first.detected_at
        )

        second_time = datetime.fromisoformat(
            second.detected_at
        )


        difference = abs(
            (first_time - second_time).total_seconds()
        )


        return difference <= window_seconds