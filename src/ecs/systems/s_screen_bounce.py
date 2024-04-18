import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_player_spawner import CPlayerSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_screen_bounce(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface)

    c_t: CTransform
    c_v: CVelocity
    c_s: CSurface
    for _, (c_t, c_v, c_s) in components:
        cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width:
            c_v.vel.x *= -1
            cuad_rect.clamp_ip(screen_rect)
            c_t.pos.x = cuad_rect.x

        if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            c_v.vel.y *= -1
            cuad_rect.clamp_ip(screen_rect)
            c_t.pos.y = cuad_rect.y


def system_enemies_screen_bounce(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CEnemySpawner)

    c_e_s: CEnemySpawner

    for entity, (c_e_s,) in components:
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


def system_players_screen_bounce(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CPlayerSpawner)
    c_p_s: CPlayerSpawner
    for _, (c_p_s,) in components:
        player = c_p_s.players[0]
        cuad_rect = player['surface'].get_rect(topleft=player['position'])
        if (cuad_rect.left < 0 or cuad_rect.right > screen_rect.width) or (
                cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height):
            cuad_rect.clamp_ip(screen_rect)
            player['position'].y = cuad_rect.y
            player['position'].x = cuad_rect.x
