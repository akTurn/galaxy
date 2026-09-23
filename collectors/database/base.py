from abc import abstractmethod

from core.collectors.base import Collector


class DatabaseCollector(Collector):

    @abstractmethod
    def detect(self) -> bool:
        """Detect whether this database type is available."""
        raise NotImplementedError
