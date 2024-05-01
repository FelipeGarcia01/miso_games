import pygame

import esper
from src.create.world_entities_strategy.world_entity_strategy import WorldEntityStrategy
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_bullet_tag import CBulletTag
from src.ecs.components.tags.c_enemy_tag import CEnemyTag, EnemyType
from src.engine.service_locator import ServiceLocator


class WorldEntityEnemy(WorldEntityStrategy):

    def create_entity(self, world: esper.World, **kwargs) -> int:
        cuad_entity = world.create_entity()
        img_surf: pygame.Surface = CSurface.from_surface(kwargs.get('image')) if kwargs.get('image') else None
        world.add_component(cuad_entity, img_surf)
        world.add_component(cuad_entity, CTransform(kwargs.get('position')))
        world.add_component(cuad_entity, CVelocity(kwargs.get('velocity')))
        if 'ASTEROID'.__eq__(kwargs.get('enemy_type')):
            world.add_component(cuad_entity, CEnemyTag(EnemyType.ASTEROID))
        if 'HUNTER'.__eq__(kwargs.get('enemy_type')):
            world.add_component(cuad_entity, CAnimation(kwargs.get('animations')))
            world.add_component(
                cuad_entity,
                CHunterState(
                    kwargs.get('enemy_data'),
                    kwargs.get('position'),
                    kwargs.get('sound_chase')
                )
            )
            world.add_component(cuad_entity, CEnemyTag(EnemyType.HUNTER))
        if kwargs.get('sound'):
            ServiceLocator.sounds_services.play(kwargs.get('sound'))
        return cuad_entity
