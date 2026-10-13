# from dataclasses import dataclass, field


# @dataclass
# class CorrelationResult:

#     finding_ids: list[str]

#     reasons: list[str] = field(
#         default_factory=list
#     )

#     confidence: float = 0.0

#     detected_window: dict = field(
#         default_factory=dict
#     )


from dataclasses import dataclass, field


@dataclass
class CorrelationResult:
    finding_ids: list[str]
    reasons: list[str] = field(default_factory=list)
    confidence: float = 0.0
    detected_window: dict = field(default_factory=dict)
    graph_path: list[dict] = field(default_factory=list)
    relationship_evidence: list[dict] = field(default_factory=list)
