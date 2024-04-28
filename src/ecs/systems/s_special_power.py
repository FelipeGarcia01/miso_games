import pygame

import esper
from src.create.prefab_bullet_loader import bullet_loader_from_file
from src.create.prefab_entities import create_world_entity
from src.ecs.components.c_especial_power import CEspecialPower
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_reload_special_power(world: esper.World, window_width: int, window_height: int):
    components = world.get_components(CEspecialPower)

    c_e_p: CEspecialPower

    for entity, (c_e_p,) in components:
        current_energy: int = c_e_p.percentage
        if current_energy < 100:
            current_energy += 1
            world.delete_entity(entity)

            color = color_by_energy(current_energy)

            create_world_entity(
                world=world, component_type="POWER_FONT",
                text=c_e_p.wording,
                font_family='sfnsmono',
                font_size=10,
                font_color=color,
                dimensions=pygame.Vector2(window_width, window_height),
                fixed='BOTTOM_LEFT',
                energy=current_energy
            )


def system_special_power_fire(world: esper.World, player: int):
    components = world.get_components(CEspecialPower)
    c_e_p: CEspecialPower
    for entity, (c_e_p,) in components:
        if c_e_p.percentage == 100:
            player_pos = world.component_for_entity(player, CTransform)
            player_size = world.component_for_entity(player, CSurface)
            player_rect = player_size.area.size
            special_bullet = bullet_loader_from_file(
                bullet_path='assets/cfg/bullet.json',
                level_path='assets/cfg/level_01.json',
                mouse_pos=pygame.mouse.get_pos(),
                player_pos=player_pos.pos,
                player_size=player_rect,
                bullet_type='SPECIAL_BULLET'
            )
            create_world_entity(
                world=world,
                component_type="BULLET",
                image=special_bullet.get('image'),
                position=special_bullet.get('position'),
                velocity=special_bullet.get('velocity'),
                sound=special_bullet.get('sound')
            )
            c_e_p.percentage = 0




def color_by_energy(energy: int) -> pygame.Color:
    if 0 < energy <= 25:
        return pygame.Color(192, 57, 43)
    if 25 < energy <= 90:
        return pygame.Color(211, 84, 0)
    if 90 < energy <= 100:
        return pygame.Color(46, 204, 113)
