from enum import Enum


class FontType(Enum):
    STATIC = 0
    DYNAMIC = 1


class CFontTag:
    def __init__(self, font_type: FontType) -> None:
        self.font_type = font_type
