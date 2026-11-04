import os
import math

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from main import Ball, Brick, Game, LEVELS, Paddle, Probe, SpecialActor, SpaceShip, WallSegment


def test_brick_hit_scales_down_and_destroys():
    brick = Brick(pygame.Rect(0, 0, 60, 20), 2, 2, 0, 0)
    assert brick.hit(0.0) is False
    assert brick.hp == 1
    assert brick.hit(0.0) is True
    assert brick.alive is False


def test_held_ball_follows_paddle():
    paddle = Paddle()
    ball = Ball(paddle)
    paddle.rect.centerx = 500
    ball.update(0.2, paddle)
    assert ball.held
    assert ball.pos.x == 500
    assert ball.pos.y == paddle.rect.top - ball.radius - 2


def test_game_builds_staggered_level():
    pygame.init()
    game = Game()
    rows = {}
    for brick in game.bricks:
        rows.setdefault(brick.row, []).append(brick.rect.x)
    assert game.bricks
    assert len(rows) >= 4
    assert rows[0][0] != rows[1][0]
    pygame.quit()


def test_radioactive_effect_expires_after_fifteen_seconds():
    pygame.init()
    game = Game()
    game.scene = "game"
    game.apply_powerup("Radioactive", 10.0)
    ball = game.balls[0]
    assert ball.effect == "Radioactive"
    assert ball.effect_until == 25.0
    game.update(0.0, 25.0, pygame.key.get_pressed())
    assert ball.effect is None
    assert ball.effect_until == 0.0
    pygame.quit()


def test_dwarf_destroy_uses_normal_drop_chance(monkeypatch):
    pygame.init()
    game = Game()
    brick = Brick(pygame.Rect(200, 200, 60, 20), 1, 1, 0, 0)
    game.bricks = [brick]
    monkeypatch.setattr("main.random.random", lambda: 0.99)
    game.destroy_brick(brick, 1.0, "Dwarf", 99)
    assert game.falling == []
    pygame.quit()


def test_alien_infection_only_reaches_immediate_row():
    pygame.init()
    game = Game()
    root = Brick(pygame.Rect(200, 200, 60, 20), 1, 1, 2, 0)
    immediate = Brick(pygame.Rect(200, 170, 60, 20), 1, 1, 1, 0)
    distant = Brick(pygame.Rect(200, 140, 60, 20), 1, 1, 0, 0)
    game.bricks = [root, immediate, distant]
    game.start_infection(root, 0.0)
    game.infect_update(2.5)
    assert immediate.infection_end == 6.0
    assert distant.infection_end == 0.0
    pygame.quit()


def test_electric_ball_discharge_is_delayed_and_not_refreshed():
    pygame.init()
    game = Game()
    target = Brick(pygame.Rect(200, 200, 60, 20), 1, 1, 1, 0)
    adjacent = Brick(pygame.Rect(200, 173, 60, 20), 1, 1, 0, 0)
    game.bricks = [target, adjacent]
    game.electricize(target, 10.0)
    game.electricize(target, 11.0)
    assert target.alive and adjacent.alive
    assert target.electro_until == 15.0
    game.infect_update(15.0)
    assert not target.alive and not adjacent.alive
    pygame.quit()


def test_probe_stays_in_orbit_while_ball_moves():
    pygame.init()
    game = Game()
    target = Ball(game.paddle)
    target.held = False
    target.pos = pygame.Vector2(300, 300)
    probe = Probe(target)
    positions = []
    for _ in range(12):
        target.pos.x += 2
        probe.update(0.1, game, 1.0)
        positions.append(probe.pos.copy())
    assert probe.orbiting
    assert math.isclose(probe.pos.distance_to(target.pos), 25.0, abs_tol=0.01)
    assert len({(round(pos.x, 2), round(pos.y, 2)) for pos in positions[-5:]}) > 1
    pygame.quit()


def test_game_has_ten_authored_levels():
    pygame.init()
    assert len(LEVELS) == 10
    game = Game()
    for index in range(len(LEVELS)):
        game.load_level(index)
        assert len(game.bricks) >= 8
    pygame.quit()


def test_wall_segments_are_separate_from_bricks_and_do_not_block_completion():
    pygame.init()
    game = Game()
    assert len(game.walls) >= 6
    assert all(isinstance(wall, WallSegment) for wall in game.walls)
    assert all(wall.rect.width >= 62 for wall in game.walls)
    assert not any(isinstance(item, WallSegment) for item in game.bricks)
    wall = game.walls[0]
    game.scene = "game"
    game.bricks = []
    game.update(0.0, 1.0, pygame.key.get_pressed())
    assert game.level_index == 1
    game.apply_powerup("Space Ship", 0.0)
    assert game.ships
    game.load_level(1)
    assert game.ships == []
    pygame.quit()


def test_special_actors_vanish_on_wall_contact_without_effect():
    pygame.init()
    game = Game()
    wall = game.walls[0]
    for kind in ("Dwarf", "Alien"):
        actor = SpecialActor(kind, game.paddle)
        actor.released = True
        actor.pos = pygame.Vector2(wall.rect.center)
        game.actors = [actor]
        score_before = game.score
        actor.update(0.0, game, 1.0)
        assert not actor.alive
        assert game.score == score_before
        assert all(brick.infection_end == 0.0 for brick in game.bricks)
    pygame.quit()


def test_space_ship_fires_two_wing_missiles_and_has_infinite_lifetime():
    pygame.init()
    game = Game()
    game.scene = "game"
    game.apply_powerup("Space Ship", 0.0)
    ship = game.ships[0]
    assert ship.flying_out
    ship.flying_out = False
    ship.mode = "Moving"
    ship.mode_until = 3.0
    ship.update(0.0, game, 3.0)
    assert ship.mode == "Aiming"
    ship.update(0.0, game, 4.0)
    assert ship.mode == "Firing"
    assert len(ship.missiles) == 2
    assert ship.missiles[0].pos.x != ship.missiles[1].pos.x
    game.update(0.016, 1000.0, pygame.key.get_pressed())
    assert ship in game.ships
    pygame.quit()


def test_space_ship_is_destroyed_by_ball_but_not_brick_contact():
    pygame.init()
    game = Game()
    game.scene = "game"
    game.apply_powerup("Space Ship", 0.0)
    ship = game.ships[0]
    brick = game.bricks[0]
    ship.pos = pygame.Vector2(brick.rect.center)
    ship.velocity = pygame.Vector2(0, 0)
    ship.update(0.0, game, 1.0)
    assert ship.alive
    ship.flying_out = False
    ball = game.balls[0]
    ball.held = False
    ball.pos = ship.pos.copy()
    ship.update(0.0, game, 3.1)
    assert not ship.alive
    pygame.quit()


def test_level_selector_starts_the_clicked_level():
    pygame.init()
    game = Game()
    game.scene = "levels"
    game.handle_event(pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": game.level_card_rects[6].center}), 0.0)
    assert game.scene == "game"
    assert game.level_index == 6
    pygame.quit()
