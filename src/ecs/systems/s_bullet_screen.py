import pygame

import esper
from src.ecs.components.c_bullet_spawner import CBulletSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_bullet_tag import CBulletTag


def system_bullet_screen(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CBulletTag, CTransform, CSurface)
    screen_rect = screen.get_rect()

    c_b_t: CBulletTag
    c_b_p: CTransform
    c_b_s: CSurface

    for entity, (c_b_t, c_b_p, c_b_s) in components:
        bullet_rect = c_b_s.surf.get_rect(topleft=c_b_p.pos)
        if not screen_rect.contains(bullet_rect):
            world.delete_entity(entity)
