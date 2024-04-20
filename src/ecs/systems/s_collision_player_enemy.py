import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_enemy_tag import CEnemyTag


def system_collision_player_enemy(world: esper.World, player: int, screen_config: tuple):
    components = world.get_components(CSurface, CTransform, CEnemyTag)
    player_position = world.component_for_entity(player, CTransform)
    player_surface = world.component_for_entity(player, CSurface)
    player_rect = CSurface.get_area_relative(player_surface.area, player_position.pos)

    c_s: CSurface
    c_t: CTransform

    for enemy_entity, (c_s, c_t, _) in components:
        enemy_rect = CSurface.get_area_relative(c_s.area, c_t.pos)

        if player_rect.colliderect(enemy_rect):
            world.delete_entity(enemy_entity)
            player_position.pos.x = screen_config[0] - player_surface.surf.get_width() / 2
            player_position.pos.y = screen_config[1] - player_surface.surf.get_height() / 2
