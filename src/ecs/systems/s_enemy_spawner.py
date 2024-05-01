import esper
from src.create.world_entities_executor import WorldEntitiesExecutor


def system_enemy_spawner(world: esper.World, enemies: list, process_time: float):
    strategy_world_entity = WorldEntitiesExecutor()
    enemies_to_spawn_list = list(
        filter(
            lambda enemy:
            process_time > enemy.get('appear_at') and not enemy.get('spawned'),
            enemies
        )
    )
    for enemy_to_spawn in enemies_to_spawn_list:
        enemy_to_spawn['spawned'] = True
        if not 'Hunter'.__eq__(enemy_to_spawn.get('type')):
            strategy_world_entity.world_entity_executor(
                world=world,
                entity_type='ENEMY_ENTITY',
                enemy_type="ASTEROID",
                position=enemy_to_spawn.get('position'),
                velocity=enemy_to_spawn.get('velocity'),
                image=enemy_to_spawn.get('image'),
                sound=enemy_to_spawn.get('sound'))
        else:
            strategy_world_entity.world_entity_executor(
                world=world,
                entity_type='ENEMY_ENTITY',
                enemy_type="HUNTER",
                enemy_data=enemy_to_spawn,
                position=enemy_to_spawn.get('position'),
                velocity=enemy_to_spawn.get('velocity'),
                image=enemy_to_spawn.get('image'),
                animations=enemy_to_spawn.get('animations'),
                sound_chase=enemy_to_spawn.get('sound_chase')
                )
