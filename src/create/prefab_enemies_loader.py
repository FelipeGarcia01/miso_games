import json
import random

import pygame


def build_enemy_data(enemy, enemy_type):
    enemy_on_x = enemy['size']['x']
    enemy_on_y = enemy['size']['y']
    enemy_size = pygame.Vector2(enemy_on_x, enemy_on_y)
    enemy_color = pygame.Color((enemy['color']['r'], enemy['color']['g'], enemy['color']['b']))
    return dict(
        type=enemy_type,
        size=enemy_size,
        color=enemy_color,
        min_velocity=enemy['velocity_min'],
        max_velocity=enemy['velocity_max'])


def build_enemy_start_data(config):
    enemy_start_position = pygame.Vector2(config['position']['x'], config['position']['y'])
    enemy_appear_at = config['time']
    return dict(type=config['enemy_type'], position=enemy_start_position, appear_at=enemy_appear_at)


def create_enemies_by_level(enemies_config: list, enemies_types: list) -> list:
    enemies: list = []
    for enemy_config in enemies_config:
        enemy = next(filter(lambda enemy_type: enemy_config.get('type').__eq__(enemy_type.get('type')), enemies_types))
        surf = pygame.Surface(enemy.get('size'))
        surf.fill(enemy.get('color'))
        velocity = random.choice([enemy['min_velocity'], enemy['max_velocity']]) * random.choice([-1, 1])
        enemies.append(
            dict(
                type=enemy.get('type'),
                position=enemy_config.get('position'),
                surface=surf,
                size=enemy.get('size'),
                color=enemy.get('color'),
                velocity=pygame.Vector2(velocity, velocity),
                appear_at=enemy_config.get('appear_at'),
                spawned=False
            )
        )
    return sorted(enemies, key=lambda x: x['appear_at'])


def load_form_files(enemies_path, level_path) -> list:
    with open(enemies_path, 'r') as enemies_loaded, open(level_path, 'r') as level_loaded:
        json_level = json.load(level_loaded)
        json_enemy = json.load(enemies_loaded)
        enemies_types = list(
            map(lambda enemy_type: build_enemy_data(json_enemy.get(enemy_type), enemy_type), json_enemy))
        enemies_config = list(map(lambda config: build_enemy_start_data(config), json_level["enemy_spawn_events"]))
    return create_enemies_by_level(enemies_config, enemies_types)
