import json
import random

import pygame


def build_explosion_data(explosion):
    image_surface = pygame.image.load(explosion.get('image')).convert_alpha()
    return dict(
        image=image_surface,
        animations=explosion.get('animations')
    )


def explosion_loader_from_file(explosion_path) -> dict:
    with open(explosion_path, "r") as explosion_loaded:
        explosion_json = json.load(explosion_loaded)
        return build_explosion_data(explosion_json)
