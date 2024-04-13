import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_player_spawner import CPlayerSpawner


def system_collision_player_enemy(world:esper.World, screen_config: tuple):
    player_spawner = world.get_component(CPlayerSpawner)
    player = player_spawner[0][1].players[0]
    player_rect = player.get('surface').get_rect(topleft=player.get('position'))

    components = world.get_components(CEnemySpawner)
    c_e_s: CEnemySpawner

    for enemy_entity, (c_e_s, ) in components:
        for enemy in c_e_s.enemies:
            enemy_rect = enemy.get('surface').get_rect(topleft=enemy.get('position'))
            if enemy_rect.colliderect(player_rect):
                c_e_s.enemies.remove(enemy)
                player['position'].x = screen_config[0] - player['surface'].get_width() / 2
                player['position'].y = screen_config[1] - player['surface'].get_height() / 2
