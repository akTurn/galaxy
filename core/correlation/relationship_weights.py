
RELATIONSHIP_WEIGHTS = {
    # Strong: direct runtime and database connections
    "owns_connection": 0.90,
    "executed_by": 0.90,
    "connected_to": 0.90,

    # Strong operational relationships
    "managed_by": 0.85,
    "manages": 0.85,
    "has_session": 0.85,
    "connects_to": 0.85,
    "executes": 0.85,
    "holds": 0.85,
    "locks": 0.85,

    # Medium: application, service, and runtime dependencies
    "provides": 0.75,
    "uses": 0.75,
    "has_process": 0.75,
    "generated_by": 0.70,
    "belongs_to": 0.70,
    "runs": 0.70,
    "parent_of": 0.65,
    "listens_on": 0.65,
    "connected_through": 0.65,

    # Data access and schema relationships
    "reads": 0.60,
    "accesses": 0.60,
    "references": 0.60,

    # Structural relationships
    "contains": 0.40,
    "has_column": 0.40,
    "has_index": 0.40,
}


def relationship_weight(relationship_type):
    return RELATIONSHIP_WEIGHTS.get(relationship_type, 0.50)
