from src.create.config_strategy.cfg_loader_strategy import CFGLoaderStrategy


class CFGLoaderInterface(CFGLoaderStrategy):

    def load_cfg(self, level_path, **kwargs):
        ...
