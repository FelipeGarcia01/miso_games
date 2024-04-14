import json
import random

import pygame


def build_player_data(player):
    player_on_x = player['size']['x']
    player_on_y = player['size']['y']
    player_size = pygame.Vector2(player_on_x, player_on_y)
    player_color = pygame.Color((player['color']['r'], player['color']['g'], player['color']['b']))
    return dict(
        size=player_size,
        color=player_color,
        velocity=player['input_velocity'])


def build_player_start_data(config, level):
    player_start_position = pygame.Vector2(level["position"]["x"] - config['size']['x'] / 2,
                                           level["position"]["y"] - config['size']['y'] / 2)
    return dict(position=player_start_position)


def create_player_by_level(player_start_data: dict, player_data: dict) -> list:
    surf = pygame.Surface(player_data.get('size'))
    surf.fill(player_data.get('color'))
    return [dict(
        position=player_start_data.get('position'),
        surface=surf,
        size=player_data.get('size'),
        color=player_data.get('color'),
        velocity=pygame.Vector2(0, 0),
        max_velocity=player_data.get('velocity')
    )]


def player_loader_from_file(players_path, level_path) -> list:
    with open(players_path, 'r') as players_loaded, open(level_path, 'r') as level_loaded:
        json_level = json.load(level_loaded)
        json_player = json.load(players_loaded)
        player_data = build_player_data(json_player)
        player_start_data = build_player_start_data(json_player, json_level["player_spawn"])

    return create_player_by_level(player_start_data, player_data)
