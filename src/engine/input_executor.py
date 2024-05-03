import esper
from src.ecs.components.c_input_command import CInputCommand
from src.engine.input_strategy.input_player_fire import InputPlayerFire
from src.engine.input_strategy.input_player_move import InputPlayerMove
from src.engine.input_strategy.input_none import InputNone
from src.engine.input_strategy.input_strategy import InputStrategy


class InputExecutor:

    def __init__(self):
        self.action_dict = {
            'PLAYER_LEFT': InputPlayerMove(),
            'PLAYER_LEFT_LETTER': InputPlayerMove(),
            'PLAYER_RIGHT': InputPlayerMove(),
            'PLAYER_RIGHT_LETTER': InputPlayerMove(),
            'PLAYER_UP': InputPlayerMove(),
            'PLAYER_UP_LETTER': InputPlayerMove(),
            'PLAYER_DOWN': InputPlayerMove(),
            'PLAYER_DOWN_LETTER': InputPlayerMove(),
            'PLAYER_FIRE': InputPlayerFire(),
            'SPECIAL_POWER': InputPlayerFire(),
        }

    def input_executor(self, world: esper.World, c_input: CInputCommand, **kwargs) -> int:
        world_entity: InputStrategy = self.action_dict.get(c_input.name, InputNone())
        return world_entity.execute_action(world, c_input, **kwargs)
