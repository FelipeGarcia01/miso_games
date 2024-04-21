import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_explosion_tag import CExplosionTag


def system_explosion(world: esper.World):
    components = world.get_components(CAnimation, CExplosionTag)
    c_a: CAnimation
    for entity_explosion, (c_a, _) in components:
        if c_a.current_frame == c_a.animations_list[c_a.current_animation].end:
            world.delete_entity(entity_explosion)
