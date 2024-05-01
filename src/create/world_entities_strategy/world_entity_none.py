from src.create.world_entities_strategy.world_entity_strategy import WorldEntityStrategy


class WorldEntityNone(WorldEntityStrategy):

    def create_entity(self, **kwargs) -> dict:
        ...