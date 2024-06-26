import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()
        self.fixed = ''

    @classmethod
    def from_text(cls, text: str, font_cfg: dict, color: pygame.Color):
        size = font_cfg.get("size")
        font = font_cfg.get('font', pygame.font.SysFont(None, size))

        c_surf = cls(pygame.Vector2(1, 1), pygame.Color(0, 0, 0, 0))
        c_surf.surf = font.render(text, True, color)
        c_surf.area = c_surf.surf.get_rect()
        c_surf.fixed = font_cfg.get('fixed')
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
