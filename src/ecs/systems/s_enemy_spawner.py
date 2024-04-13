import pygame
import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world: esper.World, screen: pygame.Surface, process_time: float):
    components = world.get_components(CEnemySpawner)
    c_e_s: CEnemySpawner

    for entity, (c_e_s, ) in components:
        enemy_to_spawn_list = list(filter(lambda enemy: process_time > enemy.get('appear_at') and not enemy.get('dead'), c_e_s.enemies))
        for enemy_to_spawn in enemy_to_spawn_list:
            screen.blit(enemy_to_spawn.get('surface'), enemy_to_spawn.get('position'))
            enemy_to_spawn['spawned'] = True
