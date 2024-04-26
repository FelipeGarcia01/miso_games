import json
import random

import pygame

from src.engine.service_locator import ServiceLocator


def build_explosion_data(explosion):
    image_surface = ServiceLocator.images_services.get(explosion.get('image'))
    return dict(
        image=image_surface,
        animations=explosion.get('animations'),
        sound=explosion.get('sound')
    )


def explosion_loader_from_file(explosion_path) -> dict:
    with open(explosion_path, "r") as explosion_loaded:
        explosion_json = json.load(explosion_loaded)
        return build_explosion_data(explosion_json)
