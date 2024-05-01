import json

import pygame

import esper
from src.create.cfg_loader_executor import CFGLoaderExecutor
from src.create.prefab_entities import create_world_entity
from src.create.world_entities_executor import WorldEntitiesExecutor
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_bullet_tag import CBulletTag
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_bullet_screen import system_bullet_screen
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_dead import system_enemy_dead
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_special_power import system_reload_special_power, system_fire_special_power, \
    system_special_power_activate
from src.ecs.systems.s_explosion import system_explosion
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_input import system_player_input
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce, system_players_screen_bounce

LEVEL_PATH = 'assets/cfg/level_01.json'


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.strategy_load_cfg = CFGLoaderExecutor()
        self.strategy_world_entity = WorldEntitiesExecutor()
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.on_pause = True
        self.delta_time = 0
        self.process_time = 0
        self.pause_entity = -1
        self.special_power_percentage = 0
        self.ecs_world = esper.World()
        with open('assets/cfg/window.json', 'r') as window_file, open(LEVEL_PATH, 'r') as level_loaded:
            json_window = json.load(window_file)
            level_pos = json.load(level_loaded)
            self.window_width = json_window.get('size').get('w')
            self.window_height = json_window.get('size').get('h')
            self.level_width = level_pos["player_spawn"]["position"]["x"]
            self.level_height = level_pos["player_spawn"]["position"]["y"]
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.SCALED)
            self.framerate = json_window.get('framerate')
            self.background_color = json_window.get('bg_color')
            self.fonts_cfg = self.strategy_load_cfg.cfg_executor(cfg_type='INTERFACE_CFG', level_path=LEVEL_PATH)
            self.enemies = self.strategy_load_cfg.cfg_executor(cfg_type='ENEMY_CFG', level_path=LEVEL_PATH)
            self.player_cfg = self.strategy_load_cfg.cfg_executor(cfg_type='PLAYER_CFG', level_path=LEVEL_PATH)
            self.explosion_cfg = self.strategy_load_cfg.cfg_executor(cfg_type='EXPLOSION_CFG', level_path=LEVEL_PATH)

    def run(self) -> None:
        self._create()
        self.is_running = True
        self.on_pause = False
        while self.is_running:
            self._process_events()
            self._calculate_time()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self.players_entity = self.strategy_world_entity.world_entity_executor(
            world=self.ecs_world, entity_type="PLAYER_ENTITY",
            image=self.player_cfg.get('image'),
            position=self.player_cfg['position'],
            velocity=self.player_cfg['velocity'],
            animations=self.player_cfg['animations'],
            sound=self.player_cfg['sound']
        )

        create_world_entity(
            world=self.ecs_world, component_type="STATIC_FONT",
            text=self.fonts_cfg.get('title').get('text'),
            font_cfg=self.fonts_cfg.get('title'),
            color=self.fonts_cfg.get('title').get('color'),
            dimensions=pygame.Vector2(self.window_width, self.window_height),
            fixed='TOP_LEFT'
        )
        create_world_entity(
            world=self.ecs_world, component_type="STATIC_FONT",
            text=self.fonts_cfg.get('general').get('text'),
            font_cfg=self.fonts_cfg.get('general'),
            color=self.fonts_cfg.get('general').get('color'),
            dimensions=pygame.Vector2(self.window_width, self.window_height),
            fixed='TOP_RIGHT'
        )
        self.special_power_entity = create_world_entity(
            world=self.ecs_world, component_type="POWER_FONT",
            text=self.fonts_cfg.get('energy').get('text'),
            font_cfg=self.fonts_cfg.get('energy'),
            color=self.fonts_cfg.get('energy').get('color'),
            dimensions=pygame.Vector2(self.window_width, self.window_height),
            fixed='BOTTOM_LEFT',
            energy=0
        )

        create_world_entity(
            world=self.ecs_world, component_type="INPUT_COMMAND",
            name="GAME_PAUSE", key=pygame.K_p
        )
        create_world_entity(
            world=self.ecs_world, component_type="INPUT_COMMAND",
            name="PLAYER_LEFT_LETTER", key=pygame.K_a
        )
        create_world_entity(
            world=self.ecs_world, component_type="INPUT_COMMAND",
            name="PLAYER_LEFT", key=pygame.K_LEFT
        )
        create_world_entity(
            world=self.ecs_world, component_type="INPUT_COMMAND",
            name="PLAYER_RIGHT_LETTER", key=pygame.K_d
        )
        create_world_entity(
            world=self.ecs_world, component_type="INPUT_COMMAND",
            name="PLAYER_RIGHT", key=pygame.K_RIGHT
        )
        create_world_entity(
            world=self.ecs_world, component_type="INPUT_COMMAND",
            name="PLAYER_UP", key=pygame.K_UP
        )
        create_world_entity(
            world=self.ecs_world, component_type="INPUT_COMMAND",
            name="PLAYER_UP_LETTER", key=pygame.K_w
        )
        create_world_entity(
            world=self.ecs_world, component_type="INPUT_COMMAND",
            name="PLAYER_DOWN_LETTER", key=pygame.K_s
        )
        create_world_entity(
            world=self.ecs_world, component_type="INPUT_COMMAND",
            name="PLAYER_DOWN", key=pygame.K_DOWN
        )
        create_world_entity(
            world=self.ecs_world, component_type="INPUT_COMMAND",
            name="PLAYER_FIRE", key=pygame.BUTTON_LEFT
        )
        create_world_entity(
            world=self.ecs_world, component_type="INPUT_COMMAND",
            name="SPECIAL_POWER", key=pygame.BUTTON_RIGHT
        )

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0 if not self.on_pause else 0
        self.process_time += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            system_player_input(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_reload_special_power(self.ecs_world, self.window_width, self.window_height, self.fonts_cfg.get('energy'))
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        system_players_screen_bounce(self.ecs_world, self.screen)
        system_bullet_screen(self.ecs_world, self.screen)
        system_enemy_spawner(self.ecs_world, self.enemies, self.process_time)
        system_collision_player_enemy(
            self.ecs_world, self.players_entity,
            (self.level_width, self.level_height),
            self.explosion_cfg)
        system_enemy_dead(self.ecs_world, self.explosion_cfg)
        system_animation(self.ecs_world, self.delta_time)
        system_player_state(self.ecs_world)
        system_hunter_state(self.ecs_world, self.players_entity)
        system_explosion(self.ecs_world)
        system_fire_special_power(self.ecs_world, self.players_entity, LEVEL_PATH)
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(
            (self.background_color.get('r'), self.background_color.get('g'), self.background_color.get('b')))
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        player_velocity_component = self.ecs_world.component_for_entity(self.players_entity, CVelocity)
        velocity = player_velocity_component.vel
        if c_input.name == "GAME_PAUSE":
            if c_input.phase == CommandPhase.START:
                self.on_pause = not self.on_pause
                if self.pause_entity == -1:
                    self.pause_entity = create_world_entity(
                        world=self.ecs_world, component_type="STATIC_FONT",
                        text=self.fonts_cfg.get('pause').get('text'),
                        font_cfg=self.fonts_cfg.get('pause'),
                        color=self.fonts_cfg.get('pause').get('color'),
                        dimensions=pygame.Vector2(self.window_width, self.window_height),
                        fixed='MIDDLE')
                else:
                    self.ecs_world.delete_entity(self.pause_entity)
                    self.pause_entity = -1
        if not self.on_pause:
            if c_input.name == "PLAYER_LEFT" or c_input.name == "PLAYER_LEFT_LETTER":
                if c_input.phase == CommandPhase.START:
                    velocity.x -= self.player_cfg.get('max_velocity', 0)
                if c_input.phase == CommandPhase.END:
                    velocity.x += self.player_cfg.get('max_velocity', 0)
            if c_input.name == "PLAYER_RIGHT" or c_input.name == "PLAYER_RIGHT_LETTER":
                if c_input.phase == CommandPhase.START:
                    velocity.x += self.player_cfg.get('max_velocity', 0)
                if c_input.phase == CommandPhase.END:
                    velocity.x -= self.player_cfg.get('max_velocity', 0)
            if c_input.name == "PLAYER_UP" or c_input.name == "PLAYER_UP_LETTER":
                if c_input.phase == CommandPhase.START:
                    velocity.y -= self.player_cfg.get('max_velocity', 0)
                if c_input.phase == CommandPhase.END:
                    velocity.y += self.player_cfg.get('max_velocity', 0)
            if c_input.name == "PLAYER_DOWN" or c_input.name == "PLAYER_DOWN_LETTER":
                if c_input.phase == CommandPhase.START:
                    velocity.y += self.player_cfg.get('max_velocity', 0)
                if c_input.phase == CommandPhase.END:
                    velocity.y -= self.player_cfg.get('max_velocity', 0)
            if c_input.name == "PLAYER_FIRE":
                player_pos = self.ecs_world.component_for_entity(self.players_entity, CTransform)
                player_size = self.ecs_world.component_for_entity(self.players_entity, CSurface)
                player_rect = player_size.area.size
                bullet = self.strategy_load_cfg.cfg_executor(
                    cfg_type='BULLET_CFG',
                    level_path=LEVEL_PATH,
                    mouse_pos=pygame.mouse.get_pos(),
                    player_pos=player_pos.pos,
                    player_size=player_rect,
                    bullet_type='STANDARD_BULLET')

                if len(self.ecs_world.get_component(CBulletTag)) < bullet.get("max_bullets"):
                    create_world_entity(
                        world=self.ecs_world,
                        component_type="BULLET",
                        image=bullet.get('image'),
                        position=bullet.get('position'),
                        velocity=bullet.get('velocity'),
                        sound=bullet.get('sound')
                    )
            if c_input.name == "SPECIAL_POWER":
                system_special_power_activate(self.ecs_world)
