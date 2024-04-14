import pygame

import esper
from src.ecs.components.c_bullet_spawner import CBulletSpawner


def system_bullet_spawner(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CBulletSpawner)
    c_b_s: CBulletSpawner

    for entity, (c_b_s,) in components:
        bullet = c_b_s.bullet
        screen.blit(bullet.get('surface'), bullet.get('position'))
