from abc import ABC, abstractmethod


class CFGLoaderStrategy(ABC):

    @abstractmethod
    def load_cfg(self, level_path, **kwargs) -> dict:
        ...
