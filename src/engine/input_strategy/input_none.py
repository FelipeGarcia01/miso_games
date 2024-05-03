import esper
from src.ecs.components.c_input_command import CInputCommand
from src.engine.input_strategy.input_strategy import InputStrategy


class InputNone(InputStrategy):

    def execute_action(self, world: esper.World, c_input: CInputCommand, **kwargs):
        ...
