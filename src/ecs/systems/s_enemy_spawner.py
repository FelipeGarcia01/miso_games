
import esper
from src.create.prefab_entities import create_world_entity


def system_enemy_spawner(world: esper.World, enemies: list, process_time: float):
    enemies_to_spawn_list = list(
        filter(
            lambda enemy:
            process_time > enemy.get('appear_at') and not enemy.get('spawned'),
            enemies
        )
    )
    for enemy_to_spawn in enemies_to_spawn_list:
        create_world_entity(world=world, component_type="ENEMIES", size=enemy_to_spawn.get('size'),
                            position=enemy_to_spawn.get('position'), color=enemy_to_spawn.get('color'),
                            velocity=enemy_to_spawn.get('velocity'))
        enemy_to_spawn['spawned'] = True
