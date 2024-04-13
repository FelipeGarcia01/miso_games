import json

import pygame

import esper
from src.create.prefab_enemies_loader import enemies_loader_from_file
from src.create.prefab_entities import create_world_entity
from src.create.prefab_player_loader import player_loader_from_file
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_player_spawner import CPlayerSpawner
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_enemies_movement, system_player_movement
from src.ecs.systems.s_player_input import system_player_input
from src.ecs.systems.s_player_spawner import system_player_spawner
from src.ecs.systems.s_screen_bounce import system_enemies_screen_bounce, system_players_screen_bounce


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.delta_time = 0
        self.process_time = 0
        self.ecs_world = esper.World()
        self.enemies = enemies_loader_from_file(enemies_path='assets/cfg/enemies.json',
                                                level_path='assets/cfg/level_01.json')
        self.player = player_loader_from_file(players_path='assets/cfg/player.json',
                                              level_path='assets/cfg/level_01.json')
        with open('assets/cfg/window.json', 'r') as window_file:
            json_window = json.load(window_file)
            self.screen = pygame.display.set_mode(
                (json_window.get('size').get('w'), json_window.get('size').get('h')), pygame.SCALED)
            self.framerate = json_window.get('framerate')
            self.background_color = json_window.get('bg_color')

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self.enemies_entity = create_world_entity(self.ecs_world, "ENEMIES", self.enemies)
        self.players_entity = create_world_entity(self.ecs_world, "PLAYER", self.player)
        create_world_entity(self.ecs_world, "INPUT_COMMAND", "PLAYER_LEFT", pygame.K_LEFT)
        create_world_entity(self.ecs_world, "INPUT_COMMAND", "PLAYER_RIGHT", pygame.K_RIGHT)
        create_world_entity(self.ecs_world, "INPUT_COMMAND", "PLAYER_UP", pygame.K_UP)
        create_world_entity(self.ecs_world, "INPUT_COMMAND", "PLAYER_DOWN", pygame.K_DOWN)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        self.process_time += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            system_player_input(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemies_movement(self.ecs_world, self.delta_time)
        system_player_movement(self.ecs_world, self.delta_time)
        system_enemies_screen_bounce(self.ecs_world, self.screen)
        system_players_screen_bounce(self.ecs_world, self.screen)

    def _draw(self):
        self.screen.fill(
            (self.background_color.get('r'), self.background_color.get('g'), self.background_color.get('b')))
        system_enemy_spawner(self.ecs_world, self.screen, self.process_time)
        system_player_spawner(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        print(f'{c_input.name} - {c_input.phase}')
        player_component = self.ecs_world.component_for_entity(entity=self.players_entity,
                                                               component_type=CPlayerSpawner)
        player = player_component.players[0]
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                player['velocity'].x -= player['max_velocity']
            if c_input.phase == CommandPhase.END:
                player['velocity'].x += player['max_velocity']
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                player['velocity'].x += player['max_velocity']
            if c_input.phase == CommandPhase.END:
                player['velocity'].x -= player['max_velocity']
        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                player['velocity'].y -= player['max_velocity']
            if c_input.phase == CommandPhase.END:
                player['velocity'].y += player['max_velocity']
        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                player['velocity'].y += player['max_velocity']
            if c_input.phase == CommandPhase.END:
                player['velocity'].y -= player['max_velocity']
