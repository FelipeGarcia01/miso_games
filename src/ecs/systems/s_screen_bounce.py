import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner

def system_screen_bounce(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CEnemySpawner)

    c_e_s: CEnemySpawner

    for entity, (c_e_s, ) in components:
        enemy_spawned_list = list(filter(lambda enemy: enemy.get('spawned'), c_e_s.enemies))
        for enemy_spawned in enemy_spawned_list:
            surf = enemy_spawned.get('surface')
            enemy_rect = surf.get_rect(topleft=enemy_spawned.get('position'))
            if enemy_rect.left < 0 or enemy_rect.right > screen_rect.width:
                enemy_spawned['velocity'].x *= -1
                enemy_rect.clamp_ip(screen_rect)
                enemy_spawned['position'].x = enemy_rect.x
            if enemy_rect.top < 0 or enemy_rect.bottom > screen_rect.height:
                enemy_spawned['velocity'].y *= -1
                enemy_rect.clamp_ip(screen_rect)
                enemy_spawned['position'].y = enemy_rect.y
