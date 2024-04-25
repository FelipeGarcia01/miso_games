import json
import random

import pygame

from src.engine.service_locator import ServiceLocator


def build_player_data(player):
    image = ServiceLocator.images_services.get(player.get('image'))
    size = image.get_size()
    size_x = size[0] / player.get('animations').get('number_frames')
    return dict(
        size=pygame.Vector2(size_x, size[1]),
        image=image,
        animations=player.get('animations'),
        velocity=player.get('input_velocity')
    )


def build_player_start_data(level, size):
    player_start_position = pygame.Vector2(
        level.get("position").get("x") - size.x / 2,
        level.get("position").get("y") - size.y / 2)
    return dict(position=player_start_position)


def create_player_by_level(player_start_data: dict, player_data: dict) -> dict:
    return dict(
        animations=player_data.get('animations'),
        position=player_start_data.get('position'),
        image=player_data.get('image'),
        velocity=pygame.Vector2(0, 0),
        max_velocity=player_data.get('velocity')
    )


def player_loader_from_file(players_path, level_path) -> dict:
    with open(players_path, 'r') as players_loaded, open(level_path, 'r') as level_loaded:
        json_level = json.load(level_loaded)
        json_player = json.load(players_loaded)
        player_data = build_player_data(json_player)
        player_start_data = build_player_start_data(json_level.get("player_spawn"), player_data.get('size'))

    return create_player_by_level(player_start_data, player_data)
