import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()

    @classmethod
    def from_text(cls, text: str,
                  font: str = None,
                  font_color: pygame.Color = None,
                  font_size: int = 10):
        if font_color is None:
            font_color = pygame.Color(255, 255, 255)

        font_family = pygame.font.SysFont(font, font_size)
        c_surf = cls(pygame.Vector2(1, 1), pygame.Color(0, 0, 0, 0))
        c_surf.surf = font_family.render(text, True, font_color)
        c_surf.area = c_surf.surf.get_rect()
        return c_surf

    @classmethod
    def from_surface(cls, surface: pygame.Surface):
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        return c_surf

    def get_area_relative(area: pygame.Rect, pos_topleft: pygame.Vector2):
        new_rect = area.copy()
        new_rect.topleft = pos_topleft.copy()
        return new_rect
