import pygame
import esper
from src.ecs.components.c_player_spawner import CPlayerSpawner


def system_player_spawner(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CPlayerSpawner)
    c_p_s: CPlayerSpawner

    for entity, (c_p_s,) in components:
        for player_to_spawn in c_p_s.players:
            screen.blit(player_to_spawn.get('surface'), player_to_spawn.get('position'))
