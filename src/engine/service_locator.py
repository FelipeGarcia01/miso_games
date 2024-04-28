from src.engine.services.fonts_service import FontsService
from src.engine.services.images_services import ImagesService
from src.engine.services.sounds_service import SoundsService


class ServiceLocator:
    images_services = ImagesService()
    sounds_services = SoundsService()
    fonts_services = FontsService()
