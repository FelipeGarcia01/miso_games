import json

import pygame

from src.create.config_strategy.cfg_loader_strategy import CFGLoaderStrategy
from src.engine.service_locator import ServiceLocator

INTERFACE_PATH = 'assets/cfg/interface.json'


def build_font_data(fonts):
    data = {}
    for _type, _cfg in fonts.items():
        font_path = _cfg.get('font')
        font_size = _cfg.get('size')
        font = ServiceLocator.fonts_services.get_font(font_path, font_size)
        color = _cfg.get('color', dict(r=255, g=255, b=255))
        color_r = color.get('r')
        color_g = color.get('g')
        color_b = color.get('b')
        data[_type] = dict(
            font=font,
            text=_cfg.get('text', 0),
            color=pygame.Color(color_r, color_g, color_b),
            size=font_size,
            fixed=_cfg.get('fixed', 'TOP_LEFT')
        )

    return data


class CFGLoaderInterface(CFGLoaderStrategy):

    def load_cfg(self, level_path, **kwargs):
        with open(INTERFACE_PATH, "r") as fonts_loaded:
            font_json = json.load(fonts_loaded)
            return build_font_data(font_json)
