import json
import random

import pygame


def build_enemy_data(enemy, enemy_type):
    return dict(
        type=enemy_type,
        image=enemy.get('image'),
        min_velocity=enemy.get('velocity_min'),
        max_velocity=enemy.get('velocity_max')
    )


def build_enemy_start_data(config):
    enemy_start_position = pygame.Vector2(config.get('position').get('x'), config.get('position').get('y'))
    enemy_appear_at = config.get('time')
    return dict(type=config.get('enemy_type'), position=enemy_start_position, appear_at=enemy_appear_at)


def create_enemies_by_level(enemies_config: list, enemies_types: list) -> list:
    enemies: list = []
    for enemy_config in enemies_config:
        enemy = next(filter(lambda enemy_type: enemy_config.get('type').__eq__(enemy_type.get('type')), enemies_types))
        velocity = random.choice([enemy.get('min_velocity'), enemy.get('max_velocity')]) * random.choice([-1, 1])
        enemies.append(
            dict(
                type=enemy.get('type'),
                position=enemy_config.get('position'),
                image=enemy.get('image'),
                velocity=pygame.Vector2(velocity, velocity),
                appear_at=enemy_config.get('appear_at'),
                spawned=False
            )
        )
    return sorted(enemies, key=lambda x: x['appear_at'])


def enemies_loader_from_file(enemies_path, level_path) -> list:
    with open(enemies_path, 'r') as enemies_loaded, open(level_path, 'r') as level_loaded:
        json_level = json.load(level_loaded)
        json_enemy = json.load(enemies_loaded)
        enemies_types = list(
            map(lambda enemy_type: build_enemy_data(json_enemy.get(enemy_type), enemy_type), json_enemy))
        enemies_config = list(map(lambda config: build_enemy_start_data(config), json_level["enemy_spawn_events"]))
    return create_enemies_by_level(enemies_config, enemies_types)
