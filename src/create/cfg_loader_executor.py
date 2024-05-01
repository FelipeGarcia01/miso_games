from src.create.config_strategy.cfg_loader_bullet import CFGLoaderBullet
from src.create.config_strategy.cfg_loader_enemy import CFGLoaderEnemy
from src.create.config_strategy.cfg_loader_explosion import CFGLoaderExplosion
from src.create.config_strategy.cfg_loader_interface import CFGLoaderInterface
from src.create.config_strategy.cfg_loader_none import CFGLoaderNone
from src.create.config_strategy.cfg_loader_player import CFGLoaderPlayer
from src.create.config_strategy.cfg_loader_strategy import CFGLoaderStrategy


class CFGLoaderExecutor:

    def __init__(self):
        self.str_dict = {
            'PLAYER_CFG': CFGLoaderPlayer(),
            'ENEMY_CFG': CFGLoaderEnemy(),
            'BULLET_CFG': CFGLoaderBullet(),
            'EXPLOSION_CFG': CFGLoaderExplosion(),
            'INTERFACE_CFG': CFGLoaderInterface()
        }

    def cfg_executor(self, cfg_type) -> dict:
        cfg_loader: CFGLoaderStrategy = self.str_dict.get(cfg_type, CFGLoaderNone())
        return cfg_loader.load_cfg()
