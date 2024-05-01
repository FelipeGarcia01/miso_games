import json

import pygame

from src.create.config_strategy.cfg_loader_strategy import CFGLoaderStrategy
from src.engine.service_locator import ServiceLocator

BULLET_PATH = 'assets/cfg/bullet.json'


def build_bullet_data(bullet, level, mouse_pos, player_pos, player_size, bullet_type: str):
    image = bullet.get('image') if 'STANDARD_BULLET'.__eq__(bullet_type) else bullet.get('special_bullet_image')
    image_surface = ServiceLocator.images_services.get(image)
    bullet_size = image_surface.get_rect().size
    pos_on_x = player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2)
    pos_on_y = player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2)
    player_pos_center = pygame.Vector2(player_pos.x + (player_size[0] / 2),
                                       player_pos.y + (player_size[1] / 2))
    velocity = (mouse_pos - player_pos_center)
    velocity = velocity.normalize() * bullet.get("velocity")
    return dict(
        position=pygame.Vector2(pos_on_x, pos_on_y),
        image=image_surface,
        velocity=velocity,
        max_bullets=level.get("player_spawn").get("max_bullets"),
        sound=bullet.get('sound')
    )


class CFGLoaderBullet(CFGLoaderStrategy):

    def load_cfg(self, level_path, **kwargs) -> dict:
        with open(BULLET_PATH, "r") as bullet_file, open(level_path, "r") as level_file:
            bullet_json = json.load(bullet_file)
            level_json = json.load(level_file)

            return build_bullet_data(
                bullet_json,
                level_json,
                kwargs.get('mouse_pos'),
                kwargs.get('player_pos'),
                kwargs.get('player_size'),
                kwargs.get('bullet_type')
            )
