import esper
from src.create.world_entities_strategy.world_entity_none import WorldEntityNone
from src.create.world_entities_strategy.world_entity_player import WorldEntityPlayer
from src.create.world_entities_strategy.world_entity_strategy import WorldEntityStrategy


class WorldEntitiesExecutor:

    def __init__(self):
        self.strategy_dict = {
            'PLAYER_ENTITY': WorldEntityPlayer()
        }

    def world_entity_executor(self, entity_type: str, world: esper.World, **kwargs) -> dict:
        world_entity: WorldEntityStrategy = self.strategy_dict.get(entity_type, WorldEntityNone())
        return world_entity.create_entity(world, **kwargs)
