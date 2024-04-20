from enum import Enum


class EnemyType(Enum):
    ASTEROID = 0
    HUNTER = 1


class CEnemyTag:
    def __init__(self, enemy_type: EnemyType) -> None:
        self.enemy_type = enemy_type
