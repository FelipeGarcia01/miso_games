import esper
from src.create.world_entities_strategy.world_entity_bullet import WorldEntityBullet
from src.create.world_entities_strategy.world_entity_enemy import WorldEntityEnemy
from src.create.world_entities_strategy.world_entity_explosion import WorldEntityExplosion
from src.create.world_entities_strategy.world_entity_input import WorldEntityInputCommand
from src.create.world_entities_strategy.world_entity_none import WorldEntityNone
from src.create.world_entities_strategy.world_entity_player import WorldEntityPlayer
from src.create.world_entities_strategy.world_entity_strategy import WorldEntityStrategy


class WorldEntitiesExecutor:

    def __init__(self):
        self.strategy_dict = {
            'PLAYER_ENTITY': WorldEntityPlayer(),
            'BULLET_ENTITY': WorldEntityBullet(),
            'EXPLOSION_ENTITY': WorldEntityExplosion(),
            'INPUT_ENTITY': WorldEntityInputCommand(),
            'ENEMY_ENTITY': WorldEntityEnemy()
        }

    def world_entity_executor(self, entity_type: str, world: esper.World, **kwargs) -> int:
        world_entity: WorldEntityStrategy = self.strategy_dict.get(entity_type, WorldEntityNone())
        return world_entity.create_entity(world, **kwargs)
