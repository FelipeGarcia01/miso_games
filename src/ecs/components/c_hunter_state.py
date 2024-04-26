from enum import Enum

import pygame

from src.engine.service_locator import ServiceLocator


class HunterState(Enum):
    IDLE = 0
    CHASE = 1
    RETURN = 2


class CHunterState:
    def __init__(self, hunter_enemy: dict, position: pygame.Vector2, chase_sound: str) -> None:
        self.hunter_enemy = hunter_enemy
        self.state = HunterState.IDLE
        self.chase_sound = chase_sound
        self.position = position.copy()
