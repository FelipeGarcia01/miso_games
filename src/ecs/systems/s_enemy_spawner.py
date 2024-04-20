
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

        if not 'Hunter'.__eq__(enemy_to_spawn.get('type')):
            create_world_entity(world=world,
                                component_type="ASTEROID",
                                position=enemy_to_spawn.get('position'),
                                velocity=enemy_to_spawn.get('velocity'),
                                image=enemy_to_spawn.get('image'))
            enemy_to_spawn['spawned'] = True
        else:
            create_world_entity(world=world,
                                component_type="HUNTER",
                                position=enemy_to_spawn.get('position'),
                                velocity=enemy_to_spawn.get('velocity'),
                                image=enemy_to_spawn.get('image'),
                                animations=enemy_to_spawn.get('animations')
                                )


