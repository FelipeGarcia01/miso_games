from enum import Enum

import pygame


class HunterState(Enum):
    IDLE = 0
    CHASE = 1
    RETURN = 2


class CHunterState:
    def __init__(self, hunter_enemy: dict, position: pygame.Vector2) -> None:
        self.hunter_enemy = hunter_enemy
        self.state = HunterState.IDLE
        self.position = position.copy()
