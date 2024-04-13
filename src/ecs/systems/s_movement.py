import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner




def system_movement(world: esper.World, delta_time):
    components = world.get_components(CEnemySpawner)
    c_e_s: CEnemySpawner

    for entity, (c_e_s,) in components:
        enemy_spawned_list = list(filter(lambda enemy: enemy.get('spawned'), c_e_s.enemies))
        for enemy_spawned in enemy_spawned_list:
            enemy_spawned['position'].x += enemy_spawned['velocity'].x * delta_time
            enemy_spawned['position'].y += enemy_spawned['velocity'].y * delta_time

