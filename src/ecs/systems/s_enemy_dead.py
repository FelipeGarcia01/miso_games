
import esper
from src.ecs.components.c_bullet_spawner import CBulletSpawner
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_dead(world: esper.World):
    bullet_component = world.get_components(CBulletSpawner)
    enemies_component = world.get_components(CEnemySpawner)

    c_b_s: CBulletSpawner
    c_e_s: CEnemySpawner

    for _, (c_e_s, ) in enemies_component:
        enemies = c_e_s.enemies
        for enemy in enemies:
            enemy_rect = enemy.get('surface').get_rect(topleft=enemy.get('position'))
            for entity_b, (c_b_s, ) in bullet_component:
                bullet_rect = c_b_s.bullet.get("surface").get_rect(topleft=c_b_s.bullet.get('position'))
                if enemy_rect.colliderect(bullet_rect):
                    c_e_s.enemies.remove(enemy)
                    world.delete_entity(entity_b)