import pygame

import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.engine.input_strategy.input_strategy import InputStrategy


def move_left(c_input, player_cfg, velocity):
    if c_input.name == "PLAYER_LEFT" or c_input.name == "PLAYER_LEFT_LETTER":
        if c_input.phase == CommandPhase.START:
            velocity.x -= player_cfg.get('max_velocity', 0)
        if c_input.phase == CommandPhase.END:
            velocity.x += player_cfg.get('max_velocity', 0)


def move_right(c_input, player_cfg, velocity):
    if c_input.name == "PLAYER_RIGHT" or c_input.name == "PLAYER_RIGHT_LETTER":
        if c_input.phase == CommandPhase.START:
            velocity.x += player_cfg.get('max_velocity', 0)
        if c_input.phase == CommandPhase.END:
            velocity.x -= player_cfg.get('max_velocity', 0)


def move_up(c_input, player_cfg, velocity):
    if c_input.name == "PLAYER_UP" or c_input.name == "PLAYER_UP_LETTER":
        if c_input.phase == CommandPhase.START:
            velocity.y -= player_cfg.get('max_velocity', 0)
        if c_input.phase == CommandPhase.END:
            velocity.y += player_cfg.get('max_velocity', 0)


def move_down(c_input, player_cfg, velocity):
    if c_input.name == "PLAYER_DOWN" or c_input.name == "PLAYER_DOWN_LETTER":
        if c_input.phase == CommandPhase.START:
            velocity.y += player_cfg.get('max_velocity', 0)
        if c_input.phase == CommandPhase.END:
            velocity.y -= player_cfg.get('max_velocity', 0)


class InputPlayerMove(InputStrategy):

    def execute_action(self, world: esper.World, c_input: CInputCommand, **kwargs):
        player_cfg = kwargs.get('player_cfg')
        player_velocity_component = world.component_for_entity(kwargs.get('player_entity'), CVelocity)
        velocity = player_velocity_component.vel
        move_left(c_input, player_cfg, velocity)
        move_right(c_input, player_cfg, velocity)
        move_down(c_input, player_cfg, velocity)
        move_up(c_input, player_cfg, velocity)
