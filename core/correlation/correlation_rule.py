from abc import ABC, abstractmethod


class CorrelationRule(ABC):
    rule_id = "base_rule"
    description = "Base correlation rule"

    @abstractmethod
    def evaluate(self, observations, graph):
        """
        Evaluate observations and graph relationships.

        Return a list of Finding objects.
        """
        raise NotImplementedError
