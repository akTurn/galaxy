from abc import ABC, abstractmethod

from core.models.observation import Observation


class Collector(ABC):

    @abstractmethod
    def collect(self) -> list[Observation]:
    #def collect(self) -> Observation:
        """Collect information and return an Observation."""
        raise NotImplementedError
