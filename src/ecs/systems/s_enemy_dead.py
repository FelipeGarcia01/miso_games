import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_bullet_tag import CBulletTag
from src.ecs.components.tags.c_enemy_tag import CEnemyTag


def system_enemy_dead(world: esper.World):
    bullet_component = world.get_components(CTransform, CSurface, CBulletTag)
    enemies_component = world.get_components(CTransform, CSurface, CEnemyTag)

    c_b_t: CTransform
    c_b_s: CSurface
    c_e_t: CTransform
    c_e_s: CSurface

    for enemy_entity, (c_e_t, c_e_s, _) in enemies_component:
        enemy_rect = c_e_s.area.copy()
        enemy_rect.topleft = c_e_t.pos
        for entity_b, (c_b_t, c_b_s, _) in bullet_component:
            bullet_rect = c_b_s.area.copy()
            bullet_rect.topleft = c_b_t.pos
            if enemy_rect.colliderect(bullet_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(entity_b)
