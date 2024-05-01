import math

import pygame

import esper
from src.create.cfg_loader_executor import CFGLoaderExecutor
from src.create.world_entities_executor import WorldEntitiesExecutor
from src.ecs.components.c_especial_power import CEspecialPower
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_reload_special_power(world: esper.World, window_width: int, window_height: int, font_cfg: dict):
    strategy_world_entity = WorldEntitiesExecutor()
    components = world.get_components(CEspecialPower)

    c_e_p: CEspecialPower

    for entity, (c_e_p,) in components:
        current_energy: int = c_e_p.percentage
        if current_energy < 100 and not c_e_p.active:
            current_energy += 1
            world.delete_entity(entity)
            color = color_by_energy(current_energy)
            strategy_world_entity.world_entity_executor(
                world=world,
                entity_type='FONT_ENTITY',
                font_type="POWER",
                text=c_e_p.wording,
                font_cfg=font_cfg,
                color=color,
                dimensions=pygame.Vector2(window_width, window_height),
                fixed='BOTTOM_LEFT',
                energy=current_energy
            )


def system_fire_special_power(world: esper.World, player: int, level_path: str):
    strategy_load_cfg = CFGLoaderExecutor()
    strategy_world_entity = WorldEntitiesExecutor()
    components = world.get_components(CEspecialPower)
    c_e_p: CEspecialPower
    for entity, (c_e_p,) in components:
        if c_e_p.active:
            player_pos = world.component_for_entity(player, CTransform)
            player_size = world.component_for_entity(player, CSurface)
            player_rect = player_size.area.size
            pos_x = player_pos.pos.x + (100 * math.cos(math.radians(c_e_p.angle)))
            pos_y = player_pos.pos.y + (100 * math.sin(math.radians(c_e_p.angle)))

            bullet = strategy_load_cfg.cfg_executor(
                cfg_type='BULLET_CFG',
                level_path=level_path,
                mouse_pos=pygame.Vector2(pos_x, pos_y),
                player_pos=player_pos.pos,
                player_size=player_rect,
                bullet_type='SPECIAL_BULLET')

            strategy_world_entity.world_entity_executor(
                world=world,
                entity_type="BULLET_ENTITY",
                image=bullet.get('image'),
                position=bullet.get('position'),
                velocity=bullet.get('velocity'),
                sound=bullet.get('sound')
            )

            c_e_p.angle += c_e_p.rotation
            c_e_p.percentage -= 1

            if c_e_p.percentage == 0:
                c_e_p.active = False


def system_special_power_activate(world: esper.World):
    components = world.get_components(CEspecialPower)
    c_e_p: CEspecialPower

    for entity, (c_e_p,) in components:
        if c_e_p.percentage == 100:
            c_e_p.active = True


def color_by_energy(energy: int) -> pygame.Color:
    if 0 < energy <= 25:
        return pygame.Color(192, 57, 43)
    if 25 < energy <= 90:
        return pygame.Color(211, 84, 0)
    if 90 < energy <= 100:
        return pygame.Color(46, 204, 113)
