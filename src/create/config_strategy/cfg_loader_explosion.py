import json

from src.create.config_strategy.cfg_loader_strategy import CFGLoaderStrategy
from src.engine.service_locator import ServiceLocator

EXPLOSION_PATH = 'assets/cfg/explosion.json'


def build_explosion_data(explosion):
    image_surface = ServiceLocator.images_services.get(explosion.get('image'))
    return dict(
        image=image_surface,
        animations=explosion.get('animations'),
        sound=explosion.get('sound')
    )


class CFGLoaderExplosion(CFGLoaderStrategy):

    def load_cfg(self, level_path, **kwargs) -> dict:
        with open(EXPLOSION_PATH, "r") as explosion_loaded:
            explosion_json = json.load(explosion_loaded)
            return build_explosion_data(explosion_json)
