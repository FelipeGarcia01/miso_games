import json

import pygame

import esper
from src.create.prefab_enemies_loader import load_form_files
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_bounce import system_screen_bounce


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.delta_time = 0
        self.process_time = 0
        self.ecs_world = esper.World()

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
        cuad_entity = self.ecs_world.create_entity()
        enemies = load_form_files(enemies_path='assets/cfg/enemies.json', level_path='assets/cfg/level_01.json')
        self.ecs_world.add_component(cuad_entity, CEnemySpawner(enemies=enemies))

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        self.process_time += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)

    def _draw(self):
        self.screen.fill(
            (self.background_color.get('r'), self.background_color.get('g'), self.background_color.get('b')))
        system_enemy_spawner(self.ecs_world, self.screen, self.process_time)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()
