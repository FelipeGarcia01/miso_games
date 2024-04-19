from pygame import Surface

import esper
import pygame
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_bullet_tag import CBulletTag
from src.ecs.components.tags.c_enemy_tag import CEnemyTag
from src.ecs.components.tags.c_player_tag import CPlayerTag


def create_world_entity(world: esper.World, component_type: str, **kargs) -> int:
    cuad_entity = world.create_entity()
    img_surf = pygame.image.load(kargs.get('image')).convert_alpha() if kargs.get('image') else None

    if component_type.__eq__("ENEMIES"):
        world.add_component(cuad_entity, CSurface.from_surface(img_surf))
        world.add_component(cuad_entity, CTransform(kargs.get('position')))
        world.add_component(cuad_entity, CVelocity(kargs.get('velocity')))
        world.add_component(cuad_entity, CEnemyTag())
    if component_type.__eq__("PLAYER"):
        world.add_component(cuad_entity, CSurface(kargs.get('size'), kargs.get('color')))
        world.add_component(cuad_entity, CTransform(kargs.get('position')))
        world.add_component(cuad_entity, CVelocity(kargs.get('velocity')))
        world.add_component(cuad_entity, CPlayerTag())
    if component_type.__eq__("INPUT_COMMAND"):
        world.add_component(cuad_entity, CInputCommand(name=kargs.get('name'), key=kargs.get('key')))
    if component_type.__eq__("BULLET"):
        world.add_component(cuad_entity, CSurface.from_surface(img_surf))
        world.add_component(cuad_entity, CTransform(kargs.get('position')))
        world.add_component(cuad_entity, CVelocity(kargs.get('velocity')))
        world.add_component(cuad_entity, CBulletTag())

    return cuad_entity
