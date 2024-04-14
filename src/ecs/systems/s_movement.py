import esper
from src.ecs.components.c_bullet_spawner import CBulletSpawner
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_player_spawner import CPlayerSpawner


def system_enemies_movement(world: esper.World, delta_time):
    components = world.get_components(CEnemySpawner)
    c_e_s: CEnemySpawner

    for entity, (c_e_s,) in components:
        enemy_spawned_list = list(filter(lambda enemy: enemy.get('spawned'), c_e_s.enemies))
        for enemy_spawned in enemy_spawned_list:
            enemy_spawned['position'].x += enemy_spawned['velocity'].x * delta_time
            enemy_spawned['position'].y += enemy_spawned['velocity'].y * delta_time


def system_player_movement(world: esper, delta_time):
    components = world.get_components(CPlayerSpawner)
    c_p_s: CPlayerSpawner

    for entity, (c_p_s,) in components:
        player = c_p_s.players[0]
        player['position'].x += player.get('velocity').x * delta_time
        player['position'].y += player.get('velocity').y * delta_time


def system_bullet_movement(world: esper, delta_time):
    components = world.get_components(CBulletSpawner)
    c_b_s: CBulletSpawner

    for entity, (c_b_s,) in components:
        bullet = c_b_s.bullet
        bullet['position'].x += bullet.get('velocity').x * delta_time
        bullet['position'].y += bullet.get('velocity').y * delta_time
