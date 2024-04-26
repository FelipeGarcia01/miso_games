import json
import random

import pygame

from src.engine.service_locator import ServiceLocator


def build_bullet_data(bullet, level, mouse_pos, player_pos, player_size):
    image_surface = ServiceLocator.images_services.get(bullet.get('image'))
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


def bullet_loader_from_file(bullet_path, level_path, mouse_pos, player_pos, player_size) -> dict:
    with open(bullet_path, "r") as bullet_file, open(level_path, "r") as level_file:
        bullet_json = json.load(bullet_file)
        level_json = json.load(level_file)

        return build_bullet_data(bullet_json, level_json, mouse_pos, player_pos, player_size)
