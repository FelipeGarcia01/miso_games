import esper
from src.create.prefab_entities import create_world_entity
from src.create.world_entities_executor import WorldEntitiesExecutor
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_bullet_tag import CBulletTag
from src.ecs.components.tags.c_enemy_tag import CEnemyTag


def system_enemy_dead(world: esper.World, explosion: dict):
    world_entity_strategy = WorldEntitiesExecutor()
    bullet_component = world.get_components(CTransform, CSurface, CBulletTag)
    enemies_component = world.get_components(CTransform, CSurface, CEnemyTag)

    c_b_t: CTransform
    c_b_s: CSurface
    c_e_t: CTransform
    c_e_s: CSurface

    for enemy_entity, (c_e_t, c_e_s, _) in enemies_component:
        enemy_rect = CSurface.get_area_relative(c_e_s.area, c_e_t.pos)
        for entity_b, (c_b_t, c_b_s, _) in bullet_component:
            bullet_rect = CSurface.get_area_relative(c_b_s.area, c_b_t.pos)
            if enemy_rect.colliderect(bullet_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(entity_b)
                world_entity_strategy.world_entity_executor(world=world,
                                                            entity_type="EXPLOSION_ENTITY",
                                                            position=c_e_t.pos,
                                                            image=explosion.get('image'),
                                                            animations=explosion.get('animations'),
                                                            sound=explosion.get('sound'))
