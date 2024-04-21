import pygame

import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_hunter_state import CHunterState, HunterState


def _do_idle_state(
        c_h_t: CTransform,
        c_h_v: CVelocity,
        c_h_a: CAnimation,
        c_h_s: CHunterState,
        player_t: CTransform,
):
    set_animation(c_h_a, 1)
    c_h_v.vel = pygame.Vector2(0, 0)
    threshold = c_h_s.hunter_enemy.get("distance_start_chase")
    if c_h_t.pos.distance_to(player_t.pos) <= threshold:
        c_h_s.state = HunterState.CHASE


def _do_chase_state(
        c_h_t: CTransform,
        c_h_v: CVelocity,
        c_h_a: CAnimation,
        c_h_s: CHunterState,
        player_t: CTransform,
):
    set_animation(c_h_a, 0)
    vel = c_h_s.hunter_enemy.get("velocity_chase")
    c_h_v.vel = (player_t.pos - c_h_t.pos).normalize() * vel
    threshold = c_h_s.hunter_enemy.get("distance_start_return")
    if c_h_s.position.distance_to(c_h_t.pos) >= threshold:
        c_h_s.state = HunterState.RETURN


def _do_return_state(
        c_h_t: CTransform,
        c_h_v: CVelocity,
        c_h_a: CAnimation,
        c_h_s: CHunterState
):
    set_animation(c_h_a, 0)
    vel = c_h_s.hunter_enemy.get("velocity_return")
    c_h_v.vel = (c_h_s.position - c_h_t.pos).normalize() * vel
    if c_h_t.pos.distance_to(c_h_s.position) < 1:
        c_h_t.pos = c_h_s.position.copy()
        c_h_s.state = HunterState.IDLE


def system_hunter_state(world: esper.World, player_entity: int):
    player_position: CTransform = world.component_for_entity(player_entity, CTransform)
    components = world.get_components(CTransform, CVelocity, CAnimation, CHunterState)
    c_h_t: CTransform
    c_h_v: CVelocity
    c_h_a: CAnimation
    c_h_s: CHunterState

    for _, (c_h_t, c_h_v, c_h_a, c_h_s) in components:
        if c_h_s.state == HunterState.IDLE:
            _do_idle_state(c_h_t, c_h_v, c_h_a, c_h_s, player_position)
        elif c_h_s.state == HunterState.CHASE:
            _do_chase_state(c_h_t, c_h_v, c_h_a, c_h_s, player_position)
        elif c_h_s.state == HunterState.RETURN:
            _do_return_state(c_h_t, c_h_v, c_h_a, c_h_s)
