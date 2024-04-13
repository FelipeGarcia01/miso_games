import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_player_spawner import CPlayerSpawner
from src.ecs.components.tags.c_enemy_tag import CEnemyTag
from src.ecs.components.tags.c_player_tag import CPlayerTag


def create_world_entity(world: esper.World, component_type: str, *args) -> int:
    cuad_entity = world.create_entity()

    if component_type.__eq__("ENEMIES"):
        world.add_component(cuad_entity, CEnemySpawner(enemies=args[0]))
        world.add_component(cuad_entity, CEnemyTag)
    if component_type.__eq__("PLAYER"):
        world.add_component(cuad_entity, CPlayerSpawner(players=args[0]))
        world.add_component(cuad_entity, CPlayerTag)

    return cuad_entity
