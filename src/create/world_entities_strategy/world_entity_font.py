import pygame

import esper
from src.create.world_entities_strategy.world_entity_strategy import WorldEntityStrategy
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_especial_power import CEspecialPower
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_bullet_tag import CBulletTag
from src.ecs.components.tags.c_enemy_tag import CEnemyTag, EnemyType
from src.ecs.components.tags.c_font_tag import CFontTag, FontType
from src.engine.service_locator import ServiceLocator


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
        y = screen.y - surf.area.height
        return pygame.Vector2(x, y)
    if 'BOTTOM_LEFT'.__eq__(fixed):
        y = screen.y - surf.area.height
        return pygame.Vector2(5, y)
    if 'BOTTOM_RIGHT'.__eq__(fixed):
        x = screen.x - surf.area.width
        y = screen.y - surf.area.height
        return pygame.Vector2(x, y)


def build_font(text: str, font_cfg: dict, dimension: pygame.Vector2, fixed: str, color: pygame.Color) -> tuple:
    font_surf: CSurface = CSurface.from_text(
        text=text, font_cfg=font_cfg, color=color)
    position: pygame.Vector2 = fixed_pos(
        dimension,
        fixed, font_surf
    )
    return font_surf, position


class WorldEntityFont(WorldEntityStrategy):

    def create_entity(self, world: esper.World, **kwargs) -> int:
        cuad_entity = world.create_entity()

        if 'STATIC'.__eq__(kwargs.get('font_type')):
            font_surf, position = build_font(
                kwargs.get('text', ''),
                kwargs.get('font_cfg'),
                kwargs.get('dimensions', pygame.Vector2(0, 0)),
                kwargs.get('fixed', 'TOP_LEFT'),
                kwargs.get('color', pygame.Color(255, 255, 255))
            )
            world.add_component(cuad_entity, font_surf)
            world.add_component(cuad_entity, CTransform(position))
            world.add_component(cuad_entity, CFontTag(FontType.STATIC))
        if 'POWER'.__eq__(kwargs.get('font_type')):
            energy = kwargs.get('energy', 0)
            wording = kwargs.get('text', '')
            font_surf, position = build_font(
                f"{wording} {energy} %",
                kwargs.get('font_cfg'),
                kwargs.get('dimensions', pygame.Vector2(0, 0)),
                kwargs.get('fixed', 'TOP_LEFT'),
                kwargs.get('color', pygame.Color(255, 255, 255))
            )
            world.add_component(cuad_entity, CEspecialPower(energy, wording))
            world.add_component(cuad_entity, font_surf)
            world.add_component(cuad_entity, CTransform(position))
            world.add_component(cuad_entity, CFontTag(FontType.DYNAMIC))
        if kwargs.get('sound'):
            ServiceLocator.sounds_services.play(kwargs.get('sound'))
        return cuad_entity
