from pygame import Surface

import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_bullet_tag import CBulletTag
from src.ecs.components.tags.c_enemy_tag import CEnemyTag, EnemyType
from src.ecs.components.tags.c_explosion_tag import CExplosionTag
from src.ecs.components.tags.c_player_tag import CPlayerTag
from src.engine.service_locator import ServiceLocator


def create_world_entity(world: esper.World, component_type: str, **kargs) -> int:
    cuad_entity = world.create_entity()
    img_surf: pygame.Surface = CSurface.from_surface(kargs.get('image')) if kargs.get('image') else None
    if component_type.__eq__("FONTS"):
        font_surf: CSurface = CSurface.from_text(text=kargs.get('text', ''), font=kargs.get('font_family', None),
                                                 font_color=kargs.get('font_color', None),
                                                 font_size=int(kargs.get('font_size', 12)))
        position: pygame.Vector2 = fixed_pos(kargs.get('dimensions', pygame.Vector2(0, 0)),
                                             kargs.get('fixed', 'TOP_LEFT'), font_surf)
        world.add_component(cuad_entity, font_surf)
        world.add_component(cuad_entity, CTransform(position))
    if component_type.__eq__("ASTEROID"):
        world.add_component(cuad_entity, img_surf)
        world.add_component(cuad_entity, CTransform(kargs.get('position')))
        world.add_component(cuad_entity, CVelocity(kargs.get('velocity')))
        world.add_component(cuad_entity, CEnemyTag(EnemyType.ASTEROID))
    if component_type.__eq__("HUNTER"):
        world.add_component(cuad_entity, img_surf)
        world.add_component(cuad_entity, CTransform(kargs.get('position')))
        world.add_component(cuad_entity, CVelocity(kargs.get('velocity')))
        world.add_component(cuad_entity, CAnimation(kargs.get('animations')))
        world.add_component(cuad_entity,
                            CHunterState(kargs.get('enemy_data'), kargs.get('position'), kargs.get('sound_chase')))
        world.add_component(cuad_entity, CEnemyTag(EnemyType.HUNTER))
    if component_type.__eq__("PLAYER"):
        world.add_component(cuad_entity, img_surf)
        world.add_component(cuad_entity, CTransform(kargs.get('position')))
        world.add_component(cuad_entity, CVelocity(kargs.get('velocity')))
        world.add_component(cuad_entity, CAnimation(kargs.get('animations')))
        world.add_component(cuad_entity, CPlayerState())
        world.add_component(cuad_entity, CPlayerTag())
    if component_type.__eq__("BULLET"):
        world.add_component(cuad_entity, img_surf)
        world.add_component(cuad_entity, CTransform(kargs.get('position')))
        world.add_component(cuad_entity, CVelocity(kargs.get('velocity')))
        world.add_component(cuad_entity, CBulletTag())
    if component_type.__eq__("EXPLOSION"):
        world.add_component(cuad_entity, img_surf)
        world.add_component(cuad_entity, CTransform(kargs.get('position')))
        world.add_component(cuad_entity, CVelocity(pygame.Vector2(0, 0)))
        world.add_component(cuad_entity, CAnimation(kargs.get('animations')))
        world.add_component(cuad_entity, CExplosionTag())
    if component_type.__eq__("INPUT_COMMAND"):
        world.add_component(cuad_entity, CInputCommand(name=kargs.get('name'), key=kargs.get('key')))

    if kargs.get('sound'):
        ServiceLocator.sounds_services.play(kargs.get('sound'))

    return cuad_entity


def fixed_pos(screen: pygame.Vector2, fixed: str, surf: CSurface) -> pygame.Vector2:
    if 'TOP_LEFT'.__eq__(fixed):
        return pygame.Vector2(5, 5)
    if 'TOP_RIGHT'.__eq__(fixed):
        x = screen.x - surf.area.width
        return pygame.Vector2(x, 5)
    if 'MIDDLE'.__eq__(fixed):
        x = (screen.x - surf.area.width) / 2
        y = (screen.y - surf.area.height) / 2
        return pygame.Vector2(x, y)
    if 'BOTTOM_MIDDLE'.__eq__(fixed):
        x = (screen.x - surf.area.width) / 2
        return pygame.Vector2(x, 5)
    if 'BOTTOM_LEFT'.__eq__(fixed):
        y = screen.y - surf.area.height
        return pygame.Vector2(5, y)
    if 'BOTTOM_RIGHT'.__eq__(fixed):
        x = screen.x - surf.area.width
        y = screen.y - surf.area.height
        return pygame.Vector2(x, y)
