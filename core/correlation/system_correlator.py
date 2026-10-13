
from datetime import datetime, timezone

from core.correlation.correlation_result import CorrelationResult
from core.correlation.relationship_weights import relationship_weight


class SystemCorrelator:

    def __init__(self, graph):
        self.graph = graph

    def correlate(self, findings):
        results = []

        for index, first in enumerate(findings):
            for second in findings[index + 1:]:
                result = self._compare(first, second)

                if result is not None:
                    results.append(result)

        return results

    def _compare(self, first, second):

        if not self._time_related(first, second):
            return None

        for entity_a in first.affected_entities:
            for entity_b in second.affected_entities:

                path = self.graph.shortest_path(
                    entity_a["entity_type"],
                    entity_a["entity_id"],
                    entity_b["entity_type"],
                    entity_b["entity_id"],
                )

                if not path:
                    continue

                # Both findings affect the same entity.
                if len(path) == 1:
                    return CorrelationResult(
                        finding_ids=[
                            first.finding_id,
                            second.finding_id,
                        ],
                        reasons=[
                            "Both findings affect the same entity",
                            "Findings occurred within time window",
                        ],
                        confidence=1.0,
                        detected_window={
                            "first": first.detected_at,
                            "second": second.detected_at,
                        },
                        graph_path=[
                            {
                                "entity_type": path[0][0],
                                "entity_id": path[0][1],
                            }
                        ],
                    )

                evidence = self._get_path_evidence(path)

                # Every path hop must have a matching stored edge.
                if len(evidence) != len(path) - 1:
                    continue

                confidence = self._calculate_confidence(evidence)

                return CorrelationResult(
                    finding_ids=[
                        first.finding_id,
                        second.finding_id,
                    ],
                    reasons=[
                        "A graph path connects the affected entities",
                        "Relationship weights contributed to the score",
                        "Findings occurred within time window",
                    ],
                    confidence=confidence,
                    detected_window={
                        "first": first.detected_at,
                        "second": second.detected_at,
                    },
                    graph_path=[
                        {
                            "entity_type": entity_type,
                            "entity_id": entity_id,
                        }
                        for entity_type, entity_id in path
                    ],
                    relationship_evidence=evidence,
                )

        return None

    def _get_path_evidence(self, path):
        # MachineGraph stores relationships as tuples:
        # (source_type, source_id, relationship_type,
        #  target_type, target_id, timestamp)
        relationships = self.graph._relationships()
        evidence = []

        for node_a, node_b in zip(path, path[1:]):
            candidates = []

            for edge in relationships:
                source = (edge[0], edge[1])
                target = (edge[3], edge[4])

                if source == node_a and target == node_b:
                    direction = "forward"
                elif source == node_b and target == node_a:
                    direction = "reverse"
                else:
                    continue

                candidates.append({
                    "source_entity_type": edge[0],
                    "source_entity_id": edge[1],
                    "relationship": edge[2],
                    "target_entity_type": edge[3],
                    "target_entity_id": edge[4],
                    "direction_in_path": direction,
                    "weight": relationship_weight(edge[2]),
                })

            if not candidates:
                continue

            # If multiple relationships connect the same nodes,
            # use the strongest one for this path hop.
            strongest = max(
                candidates,
                key=lambda item: item["weight"],
            )

            evidence.append(strongest)

        return evidence

    def _calculate_confidence(self, evidence):
        score = 1.0

        for edge in evidence:
            score *= edge["weight"]

        return round(score, 2)

    def _time_related(
        self,
        first,
        second,
        window_seconds=300,
    ):
        first_time = self._parse_time(first.detected_at)
        second_time = self._parse_time(second.detected_at)

        difference = abs(
            (first_time - second_time).total_seconds()
        )

        return difference <= window_seconds

    @staticmethod
    def _parse_time(value):
        timestamp = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        return timestamp.astimezone(timezone.utc)
