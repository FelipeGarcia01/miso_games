import esper
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_bullet_tag import CBulletTag
from src.ecs.components.tags.c_enemy_tag import CEnemyTag
from src.ecs.components.tags.c_player_tag import CPlayerTag


def create_world_entity(world: esper.World, component_type: str, **kargs) -> int:
    cuad_entity = world.create_entity()
    if component_type.__eq__("ENEMIES"):
        # world.add_component(cuad_entity, CSurface(kargs['size'], kargs['color']))
        world.add_component(cuad_entity, CTransform(kargs['position']))
        world.add_component(cuad_entity, CVelocity(kargs['velocity']))
        world.add_component(cuad_entity, CEnemyTag())
    if component_type.__eq__("PLAYER"):
        world.add_component(cuad_entity, CSurface(kargs['size'], kargs['color']))
        world.add_component(cuad_entity, CTransform(kargs['position']))
        world.add_component(cuad_entity, CVelocity(kargs['velocity']))
        world.add_component(cuad_entity, CPlayerTag())
    if component_type.__eq__("INPUT_COMMAND"):
        world.add_component(cuad_entity, CInputCommand(name=kargs['name'], key=kargs['key']))
    if component_type.__eq__("BULLET"):
        world.add_component(cuad_entity, CSurface(kargs['size'], kargs['color']))
        world.add_component(cuad_entity, CTransform(kargs['position']))
        world.add_component(cuad_entity, CVelocity(kargs['velocity']))
        world.add_component(cuad_entity, CBulletTag())

    return cuad_entity
