import pygame

import esper
from src.ecs.components.c_bullet_spawner import CBulletSpawner


def system_bullet_screen(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CBulletSpawner)
    screen_rect = screen.get_rect()

    c_b_s: CBulletSpawner
    for entity, (c_b_s, ) in components:
        bullet_rect = c_b_s.bullet.get("surface").get_rect(topleft=c_b_s.bullet.get("position"))
        if not screen_rect.contains(bullet_rect):
            world.delete_entity(entity)
