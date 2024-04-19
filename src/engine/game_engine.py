import json

import pygame

import esper
from src.create.prefab_bullet_loader import bullet_loader_from_file
from src.create.prefab_enemies_loader import enemies_loader_from_file
from src.create.prefab_entities import create_world_entity
from src.create.prefab_player_loader import player_loader_from_file
from src.ecs.components.c_bullet_spawner import CBulletSpawner
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_player_spawner import CPlayerSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_bullet_tag import CBulletTag
from src.ecs.components.tags.c_player_tag import CPlayerTag
from src.ecs.systems.s_bullet_screen import system_bullet_screen
from src.ecs.systems.s_bullet_spawner import system_bullet_spawner
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_dead import system_enemy_dead
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_input import system_player_input
from src.ecs.systems.s_player_spawner import system_player_spawner
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce, system_players_screen_bounce


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
        self.player_cfg = player_loader_from_file(players_path='assets/cfg/player.json',
                                                  level_path='assets/cfg/level_01.json')
        with open('assets/cfg/window.json', 'r') as window_file, open('assets/cfg/level_01.json', 'r') as level_loaded:
            json_window = json.load(window_file)
            level_pos = json.load(level_loaded)
            self.level_width = level_pos["player_spawn"]["position"]["x"]
            self.level_height = level_pos["player_spawn"]["position"]["y"]
            self.screen = pygame.display.set_mode((json_window.get('size').get('w'), json_window.get('size').get('h')),
                                                  pygame.SCALED)
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
        # self.enemies_entity = create_world_entity(self.ecs_world, "ENEMIES", self.enemies)
        self.players_entity = create_world_entity(world=self.ecs_world, component_type="PLAYER",
                                                  size=self.player_cfg['size'], color=self.player_cfg['color'],
                                                  position=self.player_cfg['position'],
                                                  velocity=self.player_cfg['velocity'])
        create_world_entity(world=self.ecs_world, component_type="INPUT_COMMAND", name="PLAYER_LEFT", key=pygame.K_LEFT)
        create_world_entity(world=self.ecs_world, component_type="INPUT_COMMAND", name="PLAYER_RIGHT",
                            key=pygame.K_RIGHT)
        create_world_entity(world=self.ecs_world, component_type="INPUT_COMMAND", name="PLAYER_UP", key=pygame.K_UP)
        create_world_entity(world=self.ecs_world, component_type="INPUT_COMMAND", name="PLAYER_DOWN", key=pygame.K_DOWN)
        create_world_entity(world=self.ecs_world, component_type="INPUT_COMMAND", name="PLAYER_FIRE",
                            key=pygame.BUTTON_LEFT)

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
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        system_players_screen_bounce(self.ecs_world, self.screen)
        system_bullet_screen(self.ecs_world, self.screen)
        system_enemy_spawner(self.ecs_world, self.enemies, self.process_time)
        # system_enemies_movement(self.ecs_world, self.delta_time)
        # system_player_movement(self.ecs_world, self.delta_time)
        # system_bullet_movement(self.ecs_world, self.delta_time)
        # system_enemies_screen_bounce(self.ecs_world, self.screen)
        # system_collision_player_enemy(self.ecs_world, (self.level_width, self.level_height))
        # system_enemy_dead(self.ecs_world)
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(
            (self.background_color.get('r'), self.background_color.get('g'), self.background_color.get('b')))
        # system_player_spawner(self.ecs_world, self.screen)
        # system_bullet_spawner(self.ecs_world, self.screen)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        player_velocity_component = self.ecs_world.component_for_entity(self.players_entity, CVelocity)
        velocity = player_velocity_component.vel
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                velocity.x -= self.player_cfg.get('max_velocity', 0)
            if c_input.phase == CommandPhase.END:
                velocity.x += self.player_cfg.get('max_velocity', 0)
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                velocity.x += self.player_cfg.get('max_velocity', 0)
            if c_input.phase == CommandPhase.END:
                velocity.x -= self.player_cfg.get('max_velocity', 0)
        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                velocity.y -= self.player_cfg.get('max_velocity', 0)
            if c_input.phase == CommandPhase.END:
                velocity.y += self.player_cfg.get('max_velocity', 0)
        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                velocity.y += self.player_cfg.get('max_velocity', 0)
            if c_input.phase == CommandPhase.END:
                velocity.y -= self.player_cfg.get('max_velocity', 0)
        if c_input.name == "PLAYER_FIRE":
            player_pos = self.ecs_world.component_for_entity(self.players_entity, CTransform)
            player_size = self.ecs_world.component_for_entity(self.players_entity, CSurface)
            player_rect = player_size.surf.get_rect(topleft=player_pos.pos)
            bullet = bullet_loader_from_file(
                bullet_path='assets/cfg/bullet.json',
                level_path='assets/cfg/level_01.json',
                mouse_pos=pygame.mouse.get_pos(),
                player_pos=player_pos.pos,
                player_size=player_rect
            )
            if len(self.ecs_world.get_component(CBulletTag)) < bullet.get("max_bullets"):
                create_world_entity(world=self.ecs_world, component_type="BULLET", size=bullet.get('size'),
                                    position=bullet.get('position'), color=bullet.get('color'),
                                    velocity=bullet.get('velocity'))
