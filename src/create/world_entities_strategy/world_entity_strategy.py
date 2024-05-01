from abc import ABC, abstractmethod

import esper


class WorldEntityStrategy(ABC):

    @abstractmethod
    def create_entity(self, world: esper.World, **kwargs) -> int:
        ...
