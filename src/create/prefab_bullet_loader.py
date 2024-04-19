import json
import random

import pygame


def build_bullet_data(bullet, level, mouse_pos, player_pos, player_size):
    size_on_x = bullet.get("size").get("x")
    size_on_y = bullet.get("size").get("y")
    color_r = bullet.get("color").get("r")
    color_g = bullet.get("color").get("g")
    color_b = bullet.get("color").get("b")
    pos_on_x = player_pos.x + player_size.width / 2
    pos_on_y = player_pos.y + player_size.height / 2
    position = pygame.Vector2(size_on_x, size_on_y)
    color = pygame.Color(color_r, color_g, color_b)
    surface = pygame.Surface(position)
    surface.fill(color)
    velocity = (mouse_pos - player_pos)
    velocity = velocity.normalize() * bullet.get("velocity")
    return dict(
        position=pygame.Vector2(pos_on_x, pos_on_y),
        size=pygame.Vector2(size_on_x, size_on_y),
        color=pygame.Color(color_r, color_g, color_b),
        surface=surface,
        velocity=velocity,
        max_bullets=level.get("player_spawn").get("max_bullets"))


def bullet_loader_from_file(bullet_path, level_path, mouse_pos, player_pos, player_size) -> dict:
    with open(bullet_path, "r") as bullet_file, open(level_path, "r") as level_file:
        bullet_json = json.load(bullet_file)
        level_json = json.load(level_file)

        return build_bullet_data(bullet_json, level_json, mouse_pos, player_pos, player_size)
