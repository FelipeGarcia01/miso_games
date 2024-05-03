from abc import ABC, abstractmethod

import esper
from src.ecs.components.c_input_command import CInputCommand


class InputStrategy(ABC):

    @abstractmethod
    def execute_action(self, world: esper.World, c_input: CInputCommand, **kwargs):
        ...
