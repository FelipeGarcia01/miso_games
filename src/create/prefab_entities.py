import esper
from src.ecs.components.c_bullet_spawner import CBulletSpawner
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_spawner import CPlayerSpawner
from src.ecs.components.tags.c_enemy_tag import CEnemyTag
from src.ecs.components.tags.c_player_tag import CPlayerTag


def create_world_entity(world: esper.World, component_type: str, *args) -> int:
    cuad_entity = world.create_entity()

    if component_type.__eq__("ENEMIES"):
        world.add_component(cuad_entity, CEnemySpawner(enemies=args[0]))
        world.add_component(cuad_entity, CEnemyTag())
    if component_type.__eq__("PLAYER"):
        world.add_component(cuad_entity, CPlayerSpawner(players=args[0]))
        world.add_component(cuad_entity, CPlayerTag())
    if component_type.__eq__("INPUT_COMMAND"):
        world.add_component(cuad_entity, CInputCommand(name=args[0], key=args[1]))
    if component_type.__eq__("BULLET"):
        world.add_component(cuad_entity, CBulletSpawner(bullet=args[0]))

    return cuad_entity
