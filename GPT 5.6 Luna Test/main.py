"""Neon Breakout - a self-contained Pygame breakout game.

Run with the repository interpreter:
    ..\\.venv\\Scripts\\python.exe "GPT 5.6 Luna Test\\main.py"
"""
from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pygame


WIDTH, HEIGHT = 1440, 900
PLAY_LEFT, PLAY_TOP = 40, 105
PLAY_RIGHT, PLAY_BOTTOM = 1120, 835
PADDLE_Y = PLAY_BOTTOM - 34
BRICK_W, BRICK_H = 62, 26
BRICK_GAP = 5
GRID_X, GRID_Y = 52, 135
LEVEL_COLUMNS = 15
WALL_THICKNESS = 16
FPS = 60

BG = (10, 14, 31)
PANEL = (20, 27, 51)
PANEL_2 = (29, 37, 67)
TEXT = (235, 242, 255)
MUTED = (144, 160, 195)
CYAN = (52, 225, 255)
PINK = (255, 87, 174)
PURPLE = (174, 99, 255)
GREEN = (105, 255, 174)
YELLOW = (255, 221, 75)
ORANGE = (255, 153, 78)
RED = (255, 92, 105)

POWER_COLORS = {
    "Multiball": CYAN,
    "Radioactive": GREEN,
    "Electric": YELLOW,
    "Probe": PURPLE,
    "Dwarf": ORANGE,
    "Alien": PINK,
    "Space Ship": CYAN,
}
POWER_SHORT = {
    "Multiball": "MULTI",
    "Radioactive": "RAD",
    "Electric": "ELEC",
    "Probe": "PROBE",
    "Dwarf": "DWARF",
    "Alien": "ALIEN",
    "Space Ship": "SHIP",
}

LEVELS = [
    [
        "SSSXXXXXXXXXSSS",
        "SXXYYYYYYYYYXXS",
        "SXXYZZZZZZZYXXS",
        "SXXYYYYYYYYYXXS",
        "SSSXXXXXXXXXSSS",
        "..XXXXXXXXXXX..",
        "...YYYYYYYYY...",
    ],
    [
        "SSSSSSSSSSSSSSS",
        "SXSXSXSXSXSXSXS",
        "XYYYYYYYYYYYYYX",
        "SXSXSXSXSXSXSXS",
        "XYYYYZZZZYYYYYX",
        "SXSXSXSXSXSXSXS",
        "SSSSSSSSSSSSSSS",
    ],
    [
        "....SSSSSSS....",
        "...SXXXXXXXS...",
        "..SXXYYYYYXXS..",
        ".SXXYZZZZZYXXS.",
        "SXXYYYYYYYYXXXS",
        "XXYYYYYYYYYYYXX",
        "SSSXXXXXXXXXSSS",
    ],
    [
        "SS..XXXXXXX..SS",
        "X..YYYYYYYYY..X",
        "XX..ZZZZZZZ..XX",
        "XX...YYYYY...XX",
        "XXX..ZZZZZ..XXX",
        "X...YYYYYYY...X",
        "SSSXXXXXXXXXSSS",
    ],
    [
        "SSSSS.....SSSSS",
        "SSXXXSSSSSXXXSS",
        "SXXYYYYYYYYYXXS",
        "SXXYZZZZZZZYXXS",
        "SXXYYYYYYYYYXXS",
        "SSXXXSSSSSXXXSS",
        "SSSSSXXXXXSSSSS",
    ],
    [
        "..SSSXXXXXSSS..",
        ".SXXYYYYYXXS...",
        "SXXYZZZZZYXXYXS",
        "XXY..SSSS...YXX",
        ".SXXYYYYYXXS...",
        "..SSSXXXXXSSS..",
        "...XXXXXXXXX...",
    ],
    [
        "SXSXSXSXSXSXSXS",
        "XYYYYYYYYYYYYYX",
        "SXSXSXSXSXSXSXS",
        "XZZZZZZZZZZZZZX",
        "SSSSSXXXXXSSSSS",
        "XYYYYYYYYYYYYYX",
        "SXSXSXSXSXSXSXS",
    ],
    [
        "SSSXXX...XXXSSS",
        "SXXYYYYY.YYYXXS",
        "XX..ZZZZZZZ..XX",
        "...YYYYYYYYY...",
        "XX..ZZZZZZZ..XX",
        "SXXYYYYY.YYYXXS",
        "SSSXXX...XXXSSS",
    ],
    [
        "......SSS......",
        "...SXXXXXXXS...",
        "..SXXYYYYYXXS..",
        ".SXXYZZZZZYXXS.",
        "SXXYYYYYYYYYXXS",
        "..SXXYYYYYXXS..",
        "...SXXXXXXXS...",
        "......SSS......",
    ],
    [
        "SSSZZZZZZZSSS..",
        "SXXYYYYYYYYYXXS",
        "XXYZZZZZZZZZYXX",
        "SXXYYYYYYYYYXXS",
        "SSSXXXSSSXXXSSS",
        "..XXXXXXXXXXX..",
        "...YYYYYYYYY...",
    ],
]
LEVEL_NAMES = [
    "STARFALL",
    "BUTTERFLY ARRAY",
    "NEON CROWN",
    "SERPENT RUN",
    "ORBITAL RING",
    "FORTRESS CORE",
    "ARROWHEAD",
    "WATCHER",
    "DIAMOND VAULT",
    "TIDAL WAVE",
]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def approach_angle(current: float, target: float, max_delta: float) -> float:
    delta = (target - current + math.pi) % math.tau - math.pi
    return current + clamp(delta, -max_delta, max_delta)


def draw_text(surface: pygame.Surface, font: pygame.font.Font, text: object, pos: tuple[int, int], color=TEXT, center=False) -> None:
    image = font.render(str(text), True, color)
    rect = image.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(image, rect)


class Button:
    def __init__(self, rect: pygame.Rect, label: str, accent=CYAN, small=False):
        self.rect = rect
        self.label = label
        self.accent = accent
        self.small = small
        self.hovered = False

    def update(self, mouse_pos: tuple[int, int]) -> None:
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        fill = (39, 51, 85) if self.hovered else PANEL_2
        pygame.draw.rect(surface, fill, self.rect, border_radius=8)
        pygame.draw.rect(surface, self.accent if self.hovered else (62, 79, 120), self.rect, 2, border_radius=8)
        draw_text(surface, font, self.label, self.rect.center, self.accent if self.hovered else TEXT, center=True)

    def clicked(self, event: pygame.event.Event) -> bool:
        return event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.rect.collidepoint(event.pos)


@dataclass
class WallSegment:
    """Permanent scenery, rendered and collided as a structural wall bar."""

    rect: pygame.Rect

    @property
    def center(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.center)

    def draw(self, surface: pygame.Surface) -> None:
        steel = (143, 169, 188)
        steel_dark = (42, 63, 84)
        highlight = (205, 225, 235)
        pygame.draw.rect(surface, steel_dark, self.rect, border_radius=5)
        pygame.draw.rect(surface, steel, self.rect, 2, border_radius=5)
        if self.rect.width >= self.rect.height * 2:
            pygame.draw.line(surface, steel, (self.rect.left + 4, self.rect.bottom - 4), (self.rect.right - 4, self.rect.top + 4), 2)
            for x in range(self.rect.left + 12, self.rect.right - 5, 28):
                pygame.draw.circle(surface, highlight, (x, self.rect.centery), 2)
        else:
            pygame.draw.line(surface, steel, (self.rect.left + 4, self.rect.top + 4), (self.rect.right - 4, self.rect.bottom - 4), 2)
            pygame.draw.circle(surface, highlight, self.rect.center, 2)


@dataclass
class Brick:
    rect: pygame.Rect
    hp: int
    max_hp: int
    row: int
    col: int
    electro_until: float = 0.0
    infection_end: float = 0.0
    infection_next: float = 0.0
    alive: bool = True

    @property
    def center(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.center)

    def hit(self, now: float, damage=1) -> bool:
        if not self.alive:
            return False
        if self.electro_until > now:
            return False
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def draw(self, surface: pygame.Surface, now: float) -> None:
        if not self.alive:
            return
        if self.infection_end > now:
            color = PINK
        elif self.electro_until > now:
            color = YELLOW
        else:
            color = {1: CYAN, 2: PURPLE, 3: PINK}[self.max_hp]
        ratio = clamp(self.hp / self.max_hp, 0.2, 1.0)
        inner = self.rect.inflate(-3, -3)
        pygame.draw.rect(surface, tuple(int(c * ratio) for c in color), inner, border_radius=5)
        pygame.draw.rect(surface, color, self.rect, 1, border_radius=5)
        if self.max_hp > 1:
            draw_text(surface, pygame.font.Font(None, 18), self.hp, self.rect.center, BG, center=True)


class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 68, PADDLE_Y, 136, 17)
        self.speed = 560.0
        self.multiplier = 1.0
        self.wide_until = 0.0

    def update(self, dt: float, keys, now: float) -> None:
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.rect.x += round(direction * self.speed * self.multiplier * dt)
        self.rect.left = int(clamp(self.rect.left, PLAY_LEFT + 8, PLAY_RIGHT - self.rect.width - 8))
        if self.wide_until and now >= self.wide_until:
            self.rect.width = 136
            self.wide_until = 0

    def draw(self, surface: pygame.Surface) -> None:
        shadow = self.rect.move(0, 5)
        pygame.draw.rect(surface, (27, 67, 100), shadow, border_radius=8)
        pygame.draw.rect(surface, CYAN, self.rect, border_radius=8)
        pygame.draw.rect(surface, TEXT, self.rect.inflate(-8, -8), 2, border_radius=5)


class Ball:
    def __init__(self, paddle: Paddle, velocity: Optional[pygame.Vector2] = None):
        self.radius = 8
        self.paddle = paddle
        self.pos = pygame.Vector2(paddle.rect.centerx, paddle.rect.top - self.radius - 2)
        self.velocity = velocity or pygame.Vector2(245, -350)
        self.held = True
        self.effect: Optional[str] = None
        self.effect_until = 0.0
        self.alive = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.pos.x - self.radius), round(self.pos.y - self.radius), self.radius * 2, self.radius * 2)

    def release(self) -> None:
        self.held = False

    def update(self, dt: float, paddle: Paddle) -> None:
        if self.held:
            self.pos.x = paddle.rect.centerx
            self.pos.y = paddle.rect.top - self.radius - 2
            return
        self.pos += self.velocity * dt
        if self.pos.x - self.radius <= PLAY_LEFT:
            self.pos.x = PLAY_LEFT + self.radius
            self.velocity.x = abs(self.velocity.x)
        elif self.pos.x + self.radius >= PLAY_RIGHT:
            self.pos.x = PLAY_RIGHT - self.radius
            self.velocity.x = -abs(self.velocity.x)
        if self.pos.y - self.radius <= PLAY_TOP:
            self.pos.y = PLAY_TOP + self.radius
            self.velocity.y = abs(self.velocity.y)

    def draw(self, surface: pygame.Surface, now: float) -> None:
        color = TEXT if self.effect is None else POWER_COLORS.get(self.effect, TEXT)
        if self.effect:
            pygame.draw.circle(surface, (*color, 55), self.pos, self.radius + 7)
        pygame.draw.circle(surface, color, (round(self.pos.x), round(self.pos.y)), self.radius)
        pygame.draw.circle(surface, TEXT, (round(self.pos.x - 2), round(self.pos.y - 2)), 2)


class FallingPowerUp:
    def __init__(self, kind: str, x: float, y: float):
        self.kind = kind
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(0, 0, 80, 25)
        self.rect.center = (round(x), round(y))
        self.speed = 120.0
        self.alive = True

    def update(self, dt: float, paddle: Paddle) -> bool:
        self.pos.y += self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.colliderect(paddle.rect):
            self.alive = False
            return True
        if self.pos.y > PLAY_BOTTOM + 30:
            self.alive = False
        return False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        color = POWER_COLORS[self.kind]
        pygame.draw.rect(surface, color, self.rect, border_radius=7)
        pygame.draw.rect(surface, TEXT, self.rect, 1, border_radius=7)
        draw_text(surface, font, POWER_SHORT[self.kind], self.rect.center, BG, center=True)


class Probe:
    def __init__(self, target: Ball):
        self.target = target
        self.pos = pygame.Vector2(target.pos.x - 38, target.pos.y)
        self.angle = math.atan2(self.pos.y - target.pos.y, self.pos.x - target.pos.x)
        self.orbiting = False
        self.orbit_radius = 25.0
        self.radius = 7
        self.cooldown = 0.0
        self.alive = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.pos.x - self.radius), round(self.pos.y - self.radius), self.radius * 2, self.radius * 2)

    def update(self, dt: float, game: "Game", now: float) -> None:
        if not self.target.alive:
            self.alive = False
            return
        if not self.orbiting:
            offset = self.pos - self.target.pos
            distance = offset.length()
            if distance > self.orbit_radius:
                self.pos += (self.target.pos - self.pos) * min(1.0, 260 * dt / distance)
            else:
                self.orbiting = True
                if distance > 0:
                    self.angle = math.atan2(offset.y, offset.x)
            if game.wall_collides(self.rect):
                self.alive = False
                return
        if self.orbiting:
            self.angle = (self.angle + dt * 5.5) % math.tau
            self.pos = self.target.pos + pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * self.orbit_radius
            if game.wall_collides(self.rect):
                self.alive = False
                return
            self.cooldown -= dt
            if self.cooldown <= 0:
                self.cooldown = 0.18
                game.damage_near(self.pos, 1, "Probe", now)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, PURPLE, (round(self.pos.x), round(self.pos.y)), self.radius + 4, 1)
        pygame.draw.circle(surface, PURPLE, (round(self.pos.x), round(self.pos.y)), self.radius)


class SpaceMissile:
    def __init__(self, pos: pygame.Vector2, velocity: pygame.Vector2):
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(velocity)
        self.radius = 4
        self.alive = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.pos.x - self.radius),
            round(self.pos.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def update(self, dt: float, game: "Game", now: float) -> None:
        self.pos += self.velocity * dt
        if (
            self.pos.x < PLAY_LEFT - 20
            or self.pos.x > PLAY_RIGHT + 20
            or self.pos.y < PLAY_TOP - 20
            or self.pos.y > PLAY_BOTTOM + 20
        ):
            self.alive = False
            return
        if game.wall_collides(self.rect):
            self.alive = False
            return
        for brick in game.bricks:
            if brick.alive and self.rect.colliderect(brick.rect):
                game.destroy_brick(brick, now, "Space Ship")
                self.alive = False
                return

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, CYAN, (round(self.pos.x), round(self.pos.y)), self.radius)
        pygame.draw.line(
            surface,
            TEXT,
            (round(self.pos.x), round(self.pos.y)),
            (round(self.pos.x - self.velocity.x * 0.025), round(self.pos.y - self.velocity.y * 0.025)),
            2,
        )


class SpaceShip:
    """An allied ship with a protected three-second launch and three firing modes."""

    def __init__(self, paddle: Paddle, start_time: float = 0.0):
        self.paddle = paddle
        self.pos = pygame.Vector2(paddle.rect.centerx, paddle.rect.top - 15)
        self.flyout_target = pygame.Vector2(
            clamp(paddle.rect.centerx + random.uniform(-240, 240), PLAY_LEFT + 40, PLAY_RIGHT - 40),
            PLAY_BOTTOM - 170,
        )
        self.flying_out = True
        self.invulnerable_until = start_time + 3.0
        self.velocity = pygame.Vector2(78, -48)
        self.width = 42
        self.height = 24
        self.mode = "Moving"
        self.mode_until = start_time + 3.0
        self.facing_angle = -math.pi / 2
        self.aim_angle = self.facing_angle
        self.missiles: list[SpaceMissile] = []
        self.alive = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.pos.x - self.width / 2),
            round(self.pos.y - self.height / 2),
            self.width,
            self.height,
        )

    def rebind_paddle(self, paddle: Paddle) -> None:
        self.paddle = paddle

    def _fly_out(self, dt: float, game: "Game", now: float) -> None:
        offset = self.flyout_target - self.pos
        distance = offset.length()
        if distance <= 5:
            self.pos = self.flyout_target.copy()
            self.flying_out = False
            self.mode = "Moving"
            self.mode_until = max(now, self.invulnerable_until) + random.uniform(2.0, 3.0)
            return
        step = min(distance, 125 * dt)
        movement = offset.normalize() * step
        self.pos += movement
        if game.wall_collides(self.rect) or any(brick.alive and self.rect.colliderect(brick.rect) for brick in game.bricks):
            self.pos -= movement
            self.flyout_target = self.pos + pygame.Vector2(0, -80)

    def _move(self, dt: float, game: "Game") -> None:
        horizontal_step = self.velocity.x * dt
        self.pos.x += horizontal_step
        if self.rect.left <= PLAY_LEFT:
            self.pos.x = PLAY_LEFT + self.width / 2
            self.velocity.x = abs(self.velocity.x)
        elif self.rect.right >= PLAY_RIGHT:
            self.pos.x = PLAY_RIGHT - self.width / 2
            self.velocity.x = -abs(self.velocity.x)
        elif game.wall_collides(self.rect) or any(brick.alive and self.rect.colliderect(brick.rect) for brick in game.bricks):
            self.pos.x -= horizontal_step
            self.velocity.x *= -1

        vertical_step = self.velocity.y * dt
        self.pos.y += vertical_step
        if self.rect.top <= PLAY_TOP:
            self.pos.y = PLAY_TOP + self.height / 2
            self.velocity.y = abs(self.velocity.y)
        elif self.rect.bottom >= self.paddle.rect.top - 2:
            self.pos.y = self.paddle.rect.top - self.height / 2 - 2
            self.velocity.y = -abs(self.velocity.y)
        elif game.wall_collides(self.rect) or any(brick.alive and self.rect.colliderect(brick.rect) for brick in game.bricks):
            self.pos.y -= vertical_step
            self.velocity.y *= -1

    def _choose_aim(self, game: "Game") -> None:
        targets = [brick for brick in game.bricks if brick.alive]
        if targets:
            target = min(targets, key=lambda brick: self.pos.distance_to(brick.center))
            aim = target.center - self.pos
            if aim.length_squared() == 0:
                aim = pygame.Vector2(0, -1)
            else:
                aim = aim.normalize()
        else:
            aim = pygame.Vector2(0, -1)
        self.aim_angle = math.atan2(aim.y, aim.x)

    def _fire_burst(self, game: "Game") -> None:
        # Both wing missiles share one random error relative to the ship's facing.
        fire_angle = self.facing_angle + math.radians(random.uniform(-20, 20))
        direction = pygame.Vector2(math.cos(fire_angle), math.sin(fire_angle))
        right = pygame.Vector2(-math.sin(self.facing_angle), math.cos(self.facing_angle))
        forward = pygame.Vector2(math.cos(self.facing_angle), math.sin(self.facing_angle))
        for side in (-1, 1):
            wing = self.pos + right * (side * 17) + forward * 3
            self.missiles.append(SpaceMissile(wing, direction * 270))

    def update(self, dt: float, game: "Game", now: float) -> None:
        if self.flying_out:
            self._fly_out(dt, game, now)
        elif self.mode == "Moving":
            self._move(dt, game)
            if now >= self.mode_until:
                self.mode = "Aiming"
                self.mode_until = now + 1.0
                self._choose_aim(game)
        elif self.mode == "Aiming":
            self.facing_angle = approach_angle(self.facing_angle, self.aim_angle, dt * 3.5)
            self._move(dt * 0.15, game)
            if now >= self.mode_until:
                self.mode = "Firing"
                self.mode_until = now + 0.35
                self._fire_burst(game)
        else:  # Firing
            self._move(dt * 0.25, game)
            if now >= self.mode_until:
                self.mode = "Moving"
                self.mode_until = now + random.uniform(2.0, 3.0)
                angle = random.uniform(-math.pi, math.pi)
                self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * 88

        if now >= self.invulnerable_until:
            for ball in game.balls:
                if not ball.held and self.rect.colliderect(ball.rect):
                    self.alive = False
                    game.particles.extend(Particle(self.pos, CYAN) for _ in range(12))
                    break
        for missile in self.missiles:
            missile.update(dt, game, now)
        self.missiles = [missile for missile in self.missiles if missile.alive]

    def draw(self, surface: pygame.Surface, now: float) -> None:
        sprite = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.polygon(sprite, (38, 139, 190), [(32, 10), (9, 42), (32, 35), (55, 42)])
        pygame.draw.polygon(sprite, CYAN, [(32, 14), (14, 39), (32, 33), (50, 39)])
        pygame.draw.line(sprite, TEXT, (15, 42), (49, 42), 2)
        pygame.draw.circle(sprite, TEXT, (32, 27), 4)
        rotated = pygame.transform.rotate(sprite, -math.degrees(self.facing_angle + math.pi / 2))
        surface.blit(rotated, rotated.get_rect(center=(round(self.pos.x), round(self.pos.y))))
        if self.flying_out or now < self.invulnerable_until:
            pygame.draw.circle(surface, (105, 225, 255), self.pos, 32, 1)
        for missile in self.missiles:
            missile.draw(surface)


class SpecialActor:
    def __init__(self, kind: str, paddle: Paddle):
        self.kind = kind
        self.paddle = paddle
        self.pos = pygame.Vector2(paddle.rect.center)
        self.released = False
        self.speed = 210.0
        self.angle = 0.0
        self.stop_until = 0.0
        self.alive = True
        self.target: Optional[Brick] = None

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.pos.x - 10), round(self.pos.y - 14), 20, 28)

    def release(self) -> None:
        self.released = True

    def update(self, dt: float, game: "Game", now: float) -> None:
        if not self.released:
            self.pos = pygame.Vector2(self.paddle.rect.centerx, self.paddle.rect.top - 17)
            return
        if self.kind == "Dwarf":
            if self.stop_until > now:
                self.angle += dt * 7
                game.damage_near(self.pos + pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * 32, 1, "Dwarf", now)
            else:
                self.pos.y -= self.speed * dt
                if game.wall_collides(self.rect):
                    self.alive = False
                    return
                for brick in game.bricks:
                    if brick.alive and brick.rect.collidepoint(self.pos.x, self.pos.y):
                        self.stop_until = now + 2.0
                        break
                if self.pos.y < PLAY_TOP - 50:
                    self.alive = False
        else:  # Alien
            if self.target is None:
                self.pos.y -= self.speed * dt
                if game.wall_collides(self.rect):
                    self.alive = False
                    return
                for brick in game.bricks:
                    if brick.alive and brick.rect.collidepoint(self.pos.x, self.pos.y):
                        self.target = brick
                        game.start_infection(brick, now)
                        break
                if self.pos.y < PLAY_TOP - 50:
                    self.alive = False
            else:
                if self.target.alive:
                    self.pos = pygame.Vector2(self.target.rect.center)
                else:
                    self.alive = False

    def draw(self, surface: pygame.Surface) -> None:
        color = ORANGE if self.kind == "Dwarf" else PINK
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        if self.kind == "Dwarf":
            end = self.pos + pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * 40
            pygame.draw.line(surface, TEXT, self.pos, end, 5)
            pygame.draw.line(surface, color, self.pos, end, 2)
        else:
            pygame.draw.circle(surface, TEXT, (round(self.pos.x - 4), round(self.pos.y - 3)), 2)
            pygame.draw.circle(surface, TEXT, (round(self.pos.x + 4), round(self.pos.y - 3)), 2)


class Particle:
    def __init__(self, pos: pygame.Vector2, color):
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(random.uniform(-90, 90), random.uniform(-100, 30))
        self.life = random.uniform(0.35, 0.8)
        self.max_life = self.life
        self.color = color

    def update(self, dt: float) -> None:
        self.pos += self.velocity * dt
        self.velocity.y += 180 * dt
        self.life -= dt

    def draw(self, surface: pygame.Surface) -> None:
        if self.life > 0:
            radius = max(1, round(4 * self.life / self.max_life))
            pygame.draw.circle(surface, self.color, (round(self.pos.x), round(self.pos.y)), radius)


class Game:
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.title_font = pygame.font.Font(None, 68)
        self.big_font = pygame.font.Font(None, 36)
        self.menu_buttons = [
            Button(pygame.Rect(390, 320, 260, 46), "MAIN GAME", CYAN),
            Button(pygame.Rect(390, 378, 260, 46), "DEBUG MODE", PURPLE),
            Button(pygame.Rect(390, 436, 260, 46), "SELECT LEVEL", GREEN),
            Button(pygame.Rect(390, 494, 260, 46), "LEVEL CREATOR", ORANGE),
            Button(pygame.Rect(390, 552, 260, 46), "QUIT", RED),
        ]
        self.level_card_rects = [
            pygame.Rect(30 + column * 170, 145 + row * 260, 155, 220)
            for row in range(2)
            for column in range(5)
        ]
        self.level_back_button = Button(pygame.Rect(30, 680, 155, 42), "BACK", MUTED)
        self.scene = "menu"
        self.running = True
        self.paused = False
        self.level_index = 0
        self.score = 0
        self.lives = 3
        self.combo_count = 0
        self.combo_deadline = 0.0
        self.combo_banner = ""
        self.combo_banner_until = 0.0
        self.message = ""
        self.message_until = 0.0
        self.paddle = Paddle()
        self.balls: list[Ball] = []
        self.bricks: list[Brick] = []
        self.walls: list[WallSegment] = []
        self.falling: list[FallingPowerUp] = []
        self.probes: list[Probe] = []
        self.ships: list[SpaceShip] = []
        self.actors: list[SpecialActor] = []
        self.particles: list[Particle] = []
        self.effects: dict[str, float] = {}
        self.speed_multiplier = 1.0
        self.debug_place = False
        self.debug_power = "Random"
        self.editor_grid: set[tuple[int, int]] = set()
        self.editor_buttons = [
            Button(pygame.Rect(1175, 560, 210, 42), "SAVE LEVEL", ORANGE),
            Button(pygame.Rect(1175, 612, 210, 42), "CLEAR", RED),
            Button(pygame.Rect(1175, 664, 210, 42), "BACK", MUTED),
        ]
        self.load_level(0)

    def load_level(self, index: int) -> None:
        self.level_index = index % len(LEVELS)
        self.ships.clear()
        self.bricks.clear()
        self.walls.clear()
        rows = LEVELS[self.level_index]
        for row, line in enumerate(rows):
            line = line.ljust(LEVEL_COLUMNS, ".")[:LEVEL_COLUMNS]
            offset = (BRICK_W // 2) if row % 2 else 0
            col = 0
            while col < LEVEL_COLUMNS:
                char = line[col]
                if char == "S":
                    start = col
                    while col < LEVEL_COLUMNS and line[col] == "S":
                        col += 1
                    x = GRID_X + start * (BRICK_W + BRICK_GAP) + offset
                    width = (col - start) * BRICK_W + (col - start - 1) * BRICK_GAP
                    width = min(width, PLAY_RIGHT - 10 - x)
                    if width > 0:
                        y = GRID_Y + row * (BRICK_H + 7) + (BRICK_H - WALL_THICKNESS) // 2
                        self.walls.append(WallSegment(pygame.Rect(x, y, width, WALL_THICKNESS)))
                    continue
                if char in "XYZ":
                    hp = {"X": 1, "Y": 2, "Z": 3}.get(char, 1)
                    x = GRID_X + col * (BRICK_W + BRICK_GAP) + offset
                    y = GRID_Y + row * (BRICK_H + 7)
                    if x + BRICK_W <= PLAY_RIGHT - 10:
                        self.bricks.append(Brick(pygame.Rect(x, y, BRICK_W, BRICK_H), hp, hp, row, col))
                col += 1
        self.reset_round()

    def reset_round(self) -> None:
        self.paddle = Paddle()
        self.balls = [Ball(self.paddle)]
        for ship in self.ships:
            ship.rebind_paddle(self.paddle)
        self.falling.clear()
        self.probes.clear()
        self.actors.clear()
        self.effects.clear()

    def start_game(self, debug=False, level_index: int = 0) -> None:
        self.scene = "debug" if debug else "game"
        self.ships.clear()
        self.score = 0
        self.lives = 3
        self.combo_count = 0
        self.load_level(level_index)
        self.message = "PRESS SPACE TO LAUNCH"
        self.message_until = 5.0

    def wall_collides(self, rect: pygame.Rect) -> bool:
        return any(rect.colliderect(wall.rect) for wall in self.walls)

    def choose_power(self) -> str:
        choices = list(POWER_COLORS)
        return random.choice(choices)

    def spawn_power(self, kind: str, pos: pygame.Vector2) -> None:
        if kind == "Random":
            kind = self.choose_power()
        self.falling.append(FallingPowerUp(kind, pos.x, pos.y))

    def destroy_brick(self, brick: Brick, now: float, source="Ball", damage=1) -> bool:
        if not brick.alive:
            return False
        destroyed = brick.hit(now, damage)
        if destroyed:
            self.score += {1: 100, 2: 300, 3: 400}[brick.max_hp]
            self.combo_count += 1
            self.combo_deadline = now + 2.0
            color = POWER_COLORS.get(source, CYAN)
            self.particles.extend(Particle(brick.center, color) for _ in range(8))
            if random.random() < 0.23 or source == "Debug":
                self.spawn_power(self.debug_power if source == "Debug" else "Random", brick.center)
            self.update_combo(now)
        return destroyed

    def update_combo(self, now: float) -> None:
        labels = [(25, "ULTIMATE EXTRAVAGANZA COMBO", 50000), (15, "SUPER CRUSHER COMBO", 10000), (10, "MEGA MULTI CRUSH", 5000), (6, "SUPER CRUSH", 1000)]
        for count, label, points in labels:
            if self.combo_count == count:
                self.score += points
                self.combo_banner = f"{label}  +{points:,}"
                self.combo_banner_until = now + 2.4
                break

    def apply_powerup(self, kind: str, now: float) -> None:
        self.message = f"{kind.upper()} ONLINE"
        self.message_until = now + 2.0
        if kind == "Multiball":
            self.balls.append(Ball(self.paddle, pygame.Vector2(-240, -370)))
        elif kind in ("Radioactive", "Electric"):
            target = next((ball for ball in self.balls if ball.effect is None), self.balls[0])
            target.effect = kind
            target.effect_until = now + 15.0
        elif kind == "Probe":
            target = min(self.balls, key=lambda ball: ball.pos.distance_to(self.paddle.rect.center))
            self.probes.append(Probe(target))
        elif kind == "Space Ship":
            self.ships.append(SpaceShip(self.paddle, now))
        elif kind in ("Dwarf", "Alien"):
            self.actors.append(SpecialActor(kind, self.paddle))

    def start_infection(self, brick: Brick, now: float) -> None:
        brick.infection_end = now + 3.5
        brick.infection_next = now + 2.5

    def infect_update(self, now: float) -> None:
        for brick in self.bricks:
            if brick.alive and brick.electro_until and now >= brick.electro_until:
                brick.electro_until = 0
                self.destroy_brick(brick, now, "Electric", 99)
                continue
            if not brick.alive or brick.infection_end <= 0:
                continue
            if now >= brick.infection_end:
                self.destroy_brick(brick, now, "Alien", 99)
                continue
            if brick.infection_next and now >= brick.infection_next:
                brick.infection_next = 0
                for above in self.bricks:
                    if (
                        above.alive
                        and above.row == brick.row - 1
                        and above.rect.right > brick.rect.left
                        and above.rect.left < brick.rect.right
                    ):
                        if above.infection_end <= 0:
                            self.start_infection(above, now)

    def damage_near(self, pos: pygame.Vector2, damage: int, source: str, now: float) -> None:
        nearest = [brick for brick in self.bricks if brick.alive and brick.rect.inflate(20, 20).collidepoint(pos)]
        for brick in nearest[:1]:
            self.destroy_brick(brick, now, source, damage)

    def electricize(self, brick: Brick, now: float) -> None:
        """Mark a struck brick and touching bricks for one five-second discharge."""
        for other in self.bricks:
            touching = other is brick or (
                abs(other.row - brick.row) <= 1
                and other.rect.inflate(BRICK_GAP * 2 + 2, 16).colliderect(brick.rect)
            )
            if other.alive and touching and other.electro_until <= now:
                other.electro_until = now + 5.0

    def bounce_ball(self, ball: Ball, now: float) -> None:
        if ball.held:
            return
        if ball.rect.colliderect(self.paddle.rect) and ball.velocity.y > 0:
            ball.pos.y = self.paddle.rect.top - ball.radius - 1
            relative = (ball.pos.x - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            ball.velocity = pygame.Vector2(relative * 380, -abs(ball.velocity.y))
            if ball.velocity.length() < 250:
                ball.velocity.scale_to_length(250)
        for wall in self.walls:
            if not ball.rect.colliderect(wall.rect):
                continue
            if abs(ball.pos.y - wall.rect.top) < wall.rect.height or abs(ball.pos.y - wall.rect.bottom) < wall.rect.height:
                ball.velocity.y *= -1
            else:
                ball.velocity.x *= -1
            return
        for brick in self.bricks:
            if not brick.alive or not ball.rect.colliderect(brick.rect):
                continue
            if ball.effect == "Electric":
                self.electricize(brick, now)
            else:
                self.destroy_brick(brick, now, "Ball", 99 if ball.effect == "Radioactive" else 1)
            if abs(ball.pos.y - brick.rect.top) < 13 or abs(ball.pos.y - brick.rect.bottom) < 13:
                ball.velocity.y *= -1
            else:
                ball.velocity.x *= -1
            break

    def place_debug_brick(self, pos: tuple[int, int]) -> None:
        x, y = pos
        row = round((y - GRID_Y) / (BRICK_H + 7))
        offset = (BRICK_W // 2) if row % 2 else 0
        col = round((x - GRID_X - offset) / (BRICK_W + BRICK_GAP))
        rect = pygame.Rect(GRID_X + col * (BRICK_W + BRICK_GAP) + offset, GRID_Y + row * (BRICK_H + 7), BRICK_W, BRICK_H)
        if rect.left < PLAY_LEFT or rect.right > PLAY_RIGHT or rect.top < PLAY_TOP or rect.bottom > PLAY_BOTTOM - 100:
            return
        for brick in self.bricks:
            if brick.rect == rect:
                return
        self.bricks.append(Brick(rect, 2, 2, row, col))

    def debug_destroy_one(self, now: float) -> None:
        brick = next((b for b in reversed(self.bricks) if b.alive), None)
        if brick:
            self.destroy_brick(brick, now, "Debug", 99)
            self.message = f"DESTROYED -> {self.debug_power.upper()}"
            self.message_until = now + 2.0

    def update(self, dt: float, now: float, keys) -> None:
        if self.scene not in ("game", "debug") or self.paused:
            return
        self.paddle.update(dt, keys, now)
        for ball in self.balls:
            if ball.effect and now >= ball.effect_until:
                ball.effect = None
                ball.effect_until = 0.0
            ball.update(dt * self.speed_multiplier, self.paddle)
            self.bounce_ball(ball, now)
        for ship in self.ships:
            ship.update(dt * self.speed_multiplier, self, now)
        self.ships = [ship for ship in self.ships if ship.alive]
        self.balls = [ball for ball in self.balls if ball.pos.y < PLAY_BOTTOM + 40 and ball.alive]
        if not self.balls:
            self.lives -= 1
            if self.lives > 0:
                self.reset_round()
                self.message = "BALL LOST - PRESS SPACE"
                self.message_until = now + 2.0
            else:
                self.scene = "menu"
                self.message = "GAME OVER"
                self.message_until = now + 3.0
        for power in self.falling:
            if power.update(dt, self.paddle):
                self.apply_powerup(power.kind, now)
        self.falling = [power for power in self.falling if power.alive]
        for probe in self.probes:
            probe.update(dt, self, now)
        self.probes = [probe for probe in self.probes if probe.alive]
        for actor in self.actors:
            actor.update(dt, self, now)
        self.actors = [actor for actor in self.actors if actor.alive]
        self.infect_update(now)
        for particle in self.particles:
            particle.update(dt)
        self.particles = [particle for particle in self.particles if particle.life > 0]
        if self.combo_deadline and now > self.combo_deadline:
            if self.combo_count >= 6:
                self.combo_banner = f"COMBO x{self.combo_count}"
                self.combo_banner_until = now + 2.0
            self.combo_count = 0
            self.combo_deadline = 0
        if not any(brick.alive for brick in self.bricks):
            self.load_level(self.level_index + 1)
            self.message = f"LEVEL {self.level_index + 1}: {LEVEL_NAMES[self.level_index]}"
            self.message_until = now + 2.0

    def handle_game_event(self, event: pygame.event.Event, now: float) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scene = "menu"
            elif event.key == pygame.K_p:
                self.paused = not self.paused
            elif event.key == pygame.K_SPACE:
                for ball in self.balls:
                    if ball.held:
                        ball.release()
                for actor in self.actors:
                    if not actor.released:
                        actor.release()
        if self.scene == "debug":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.debug_place:
                self.place_debug_brick(event.pos)
            if event.type == pygame.MOUSEMOTION and self.debug_place and event.buttons[0]:
                self.place_debug_brick(event.pos)

    def draw_background(self, surface: pygame.Surface) -> None:
        surface.fill(BG)
        for x in range(0, WIDTH, 40):
            pygame.draw.line(surface, (14, 22, 43), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(surface, (14, 22, 43), (0, y), (WIDTH, y))
        pygame.draw.rect(surface, (25, 34, 62), pygame.Rect(PLAY_LEFT - 2, PLAY_TOP - 2, PLAY_RIGHT - PLAY_LEFT + 4, PLAY_BOTTOM - PLAY_TOP + 4), 2, border_radius=10)

    def draw_hud(self, surface: pygame.Surface, now: float) -> None:
        draw_text(surface, self.font, f"SCORE  {self.score:,}", (38, 25), CYAN)
        draw_text(surface, self.font, f"LIVES  {'● ' * self.lives}", (280, 25), PINK)
        draw_text(surface, self.font, f"LEVEL {self.level_index + 1}/10  {LEVEL_NAMES[self.level_index]}", (450, 25), PURPLE)
        draw_text(surface, self.font, "P: PAUSE   ESC: MENU", (650, 25), MUTED)
        if self.combo_count:
            draw_text(surface, self.font, f"COMBO x{self.combo_count}", (PLAY_RIGHT - 140, PLAY_BOTTOM - 30), YELLOW)
        if self.message_until > now:
            draw_text(surface, self.big_font, self.message, ((PLAY_LEFT + PLAY_RIGHT) // 2, PLAY_BOTTOM - 66), TEXT, center=True)
        if self.combo_banner_until > now:
            draw_text(surface, self.big_font, self.combo_banner, ((PLAY_LEFT + PLAY_RIGHT) // 2, 70), YELLOW, center=True)

    def draw_game(self, surface: pygame.Surface, now: float) -> None:
        self.draw_background(surface)
        self.draw_hud(surface, now)
        for wall in self.walls:
            wall.draw(surface)
        for brick in self.bricks:
            brick.draw(surface, now)
        for particle in self.particles:
            particle.draw(surface)
        self.paddle.draw(surface)
        for ball in self.balls:
            ball.draw(surface, now)
        for ship in self.ships:
            ship.draw(surface, now)
        for power in self.falling:
            power.draw(surface, self.small_font)
        for probe in self.probes:
            probe.draw(surface)
        for actor in self.actors:
            actor.draw(surface)
        if self.paused:
            overlay = pygame.Surface((PLAY_RIGHT - PLAY_LEFT, PLAY_BOTTOM - PLAY_TOP), pygame.SRCALPHA)
            overlay.fill((4, 7, 18, 190))
            surface.blit(overlay, (PLAY_LEFT, PLAY_TOP))
            draw_text(surface, self.title_font, "PAUSED", ((PLAY_LEFT + PLAY_RIGHT) // 2, 365), TEXT, center=True)
        if self.scene == "debug":
            self.draw_debug_panel(surface)

    def draw_debug_panel(self, surface: pygame.Surface) -> None:
        panel = pygame.Rect(1150, 105, 260, 450)
        pygame.draw.rect(surface, PANEL, panel, border_radius=10)
        pygame.draw.rect(surface, PURPLE, panel, 2, border_radius=10)
        draw_text(surface, self.big_font, "DEBUG MODE", (1175, 126), PURPLE)
        draw_text(surface, self.small_font, "TOOLS", (1175, 174), MUTED)
        draw_text(surface, self.font, "Powerup", (1175, 200), TEXT)
        pygame.draw.rect(surface, PANEL_2, pygame.Rect(1175, 226, 210, 35), border_radius=5)
        draw_text(surface, self.small_font, self.debug_power, (1186, 236), POWER_COLORS.get(self.debug_power, TEXT))
        draw_text(surface, self.small_font, "click to cycle", (1285, 236), MUTED)
        draw_text(surface, self.font, "Speed", (1175, 285), TEXT)
        draw_text(surface, self.font, f"x{self.speed_multiplier:g}", (1270, 285), CYAN)
        for i, value in enumerate((0.25, 0.5, 1, 1.5, 2)):
            rect = pygame.Rect(1175 + (i % 3) * 68, 315 + (i // 3) * 38, 60, 29)
            active = self.speed_multiplier == value
            pygame.draw.rect(surface, CYAN if active else PANEL_2, rect, border_radius=5)
            draw_text(surface, self.small_font, f"x{value:g}", rect.center, BG if active else TEXT, center=True)
        destroy = Button(pygame.Rect(1175, 400, 210, 38), "DESTROY + DROP", PINK, True)
        destroy.draw(surface, self.small_font)
        place = Button(pygame.Rect(1175, 450, 210, 38), "PAINT BRICKS", ORANGE, True)
        place.draw(surface, self.small_font)
        if self.debug_place:
            draw_text(surface, self.small_font, "PAINT ON: drag in playfield", (1175, 515), ORANGE)
        else:
            draw_text(surface, self.small_font, "PAINT OFF", (1175, 515), MUTED)

    def draw_menu(self, surface: pygame.Surface) -> None:
        self.draw_background(surface)
        draw_text(surface, self.title_font, "NEON BREAKOUT", (WIDTH // 2, 145), CYAN, center=True)
        draw_text(surface, self.font, "A kinetic brick-crushing arcade lab", (WIDTH // 2, 205), MUTED, center=True)
        for button in self.menu_buttons:
            button.draw(surface, self.font)
        draw_text(surface, self.small_font, "SPACE launches held balls and tools  •  A/D or arrow keys move", (WIDTH // 2, 650), MUTED, center=True)
        draw_text(surface, self.small_font, "Ten creative levels  •  seven powerups  •  combo scoring", (WIDTH // 2, 672), MUTED, center=True)

    def draw_level_thumbnail(self, surface: pygame.Surface, rect: pygame.Rect, level_index: int) -> None:
        pygame.draw.rect(surface, BG, rect, border_radius=6)
        rows = LEVELS[level_index]
        rows = [row.ljust(LEVEL_COLUMNS, ".")[:LEVEL_COLUMNS] for row in LEVELS[level_index]]
        max_columns = LEVEL_COLUMNS
        cell_width = rect.width / max_columns
        cell_height = min(18, (rect.height - 8) / len(rows))
        for row_index, line in enumerate(rows):
            for column, char in enumerate(line):
                if char not in "XYZS":
                    continue
                color = {"X": CYAN, "Y": PURPLE, "Z": PINK, "S": (116, 137, 157)}[char]
                tile = pygame.Rect(
                    round(rect.left + column * cell_width),
                    round(rect.top + row_index * cell_height),
                    max(2, round(cell_width - 2)),
                    max(3, round(cell_height - 2)),
                )
                pygame.draw.rect(surface, color, tile, border_radius=2)

    def draw_level_select(self, surface: pygame.Surface) -> None:
        self.draw_background(surface)
        draw_text(surface, self.title_font, "SELECT LEVEL", (WIDTH // 2, 58), GREEN, center=True)
        draw_text(surface, self.small_font, "Choose a pre-created scenario to start from", (WIDTH // 2, 101), MUTED, center=True)
        mouse_pos = pygame.mouse.get_pos()
        for level_index, card in enumerate(self.level_card_rects):
            hovered = card.collidepoint(mouse_pos)
            pygame.draw.rect(surface, (39, 51, 85) if hovered else PANEL, card, border_radius=9)
            pygame.draw.rect(surface, GREEN if hovered else (62, 79, 120), card, 2, border_radius=9)
            draw_text(surface, self.font, f"LEVEL {level_index + 1}", (card.centerx, card.top + 17), GREEN, center=True)
            draw_text(surface, self.small_font, LEVEL_NAMES[level_index], (card.centerx, card.top + 38), TEXT, center=True)
            thumbnail = card.inflate(-16, -72)
            thumbnail.top += 20
            thumbnail.height -= 20
            self.draw_level_thumbnail(surface, thumbnail, level_index)
            draw_text(surface, self.small_font, "CLICK TO PLAY", (card.centerx, card.bottom - 13), MUTED, center=True)
        self.level_back_button.update(mouse_pos)
        self.level_back_button.draw(surface, self.small_font)

    def draw_editor(self, surface: pygame.Surface) -> None:
        self.draw_background(surface)
        draw_text(surface, self.title_font, "LEVEL CREATOR", (34, 25), ORANGE)
        draw_text(surface, self.small_font, "Click or drag to paint 1/2/3 HP bricks. Rows use the same staggered pattern as gameplay.", (40, 76), MUTED)
        for row in range(15):
            offset = BRICK_W // 2 if row % 2 else 0
            for col in range(LEVEL_COLUMNS):
                rect = pygame.Rect(GRID_X + col * (BRICK_W + BRICK_GAP) + offset, GRID_Y + row * (BRICK_H + 7), BRICK_W, BRICK_H)
                if rect.right > PLAY_RIGHT - 10 or rect.bottom > PLAY_BOTTOM - 10:
                    continue
                key = (row, col)
                filled = key in self.editor_grid
                pygame.draw.rect(surface, PURPLE if filled else PANEL_2, rect, border_radius=4)
                pygame.draw.rect(surface, (79, 94, 135), rect, 1, border_radius=4)
        pygame.draw.rect(surface, PANEL, pygame.Rect(1150, 105, 260, 630), border_radius=10)
        pygame.draw.rect(surface, ORANGE, pygame.Rect(1150, 105, 260, 630), 2, border_radius=10)
        draw_text(surface, self.big_font, "CUSTOM SCENARIO", (1175, 131), ORANGE)
        draw_text(surface, self.font, "Click a filled tile", (1175, 191), TEXT)
        draw_text(surface, self.small_font, "again to remove it", (1175, 216), MUTED)
        draw_text(surface, self.font, "Saves to custom_level.json", (1175, 271), TEXT)
        for button in self.editor_buttons:
            button.draw(surface, self.small_font)

    def handle_menu(self, event: pygame.event.Event) -> None:
        for i, button in enumerate(self.menu_buttons):
            if button.clicked(event):
                if i == 0:
                    self.start_game(False)
                elif i == 1:
                    self.start_game(True)
                elif i == 2:
                    self.scene = "levels"
                elif i == 3:
                    self.scene = "editor"
                else:
                    self.running = False

    def handle_level_select(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.scene = "menu"
            return
        if self.level_back_button.clicked(event):
            self.scene = "menu"
            return
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for level_index, card in enumerate(self.level_card_rects):
                if card.collidepoint(event.pos):
                    self.start_game(False, level_index)
                    return

    def handle_debug_panel(self, event: pygame.event.Event, now: float) -> None:
        if event.type != pygame.MOUSEBUTTONUP or event.button != 1:
            return
        if pygame.Rect(1175, 226, 210, 35).collidepoint(event.pos):
            choices = ["Random", *POWER_COLORS]
            self.debug_power = choices[(choices.index(self.debug_power) + 1) % len(choices)]
        for i, value in enumerate((0.25, 0.5, 1, 1.5, 2)):
            rect = pygame.Rect(1175 + (i % 3) * 68, 315 + (i // 3) * 38, 60, 29)
            if rect.collidepoint(event.pos):
                self.speed_multiplier = value
        if pygame.Rect(1175, 400, 210, 38).collidepoint(event.pos):
            self.debug_destroy_one(now)
        if pygame.Rect(1175, 450, 210, 38).collidepoint(event.pos):
            self.debug_place = not self.debug_place

    def handle_editor(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.editor_paint(event.pos, toggle=True)
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            self.editor_paint(event.pos)
        for i, button in enumerate(self.editor_buttons):
            if button.clicked(event):
                if i == 0:
                    self.save_editor_level()
                elif i == 1:
                    self.editor_grid.clear()
                else:
                    self.scene = "menu"

    def editor_paint(self, pos: tuple[int, int], toggle=False) -> None:
        x, y = pos
        for row in range(15):
            offset = BRICK_W // 2 if row % 2 else 0
            for col in range(LEVEL_COLUMNS):
                rect = pygame.Rect(GRID_X + col * (BRICK_W + BRICK_GAP) + offset, GRID_Y + row * (BRICK_H + 7), BRICK_W, BRICK_H)
                if rect.collidepoint(x, y):
                    key = (row, col)
                    if toggle and key in self.editor_grid:
                        self.editor_grid.remove(key)
                    elif key not in self.editor_grid:
                        self.editor_grid.add(key)
                    return

    def save_editor_level(self) -> None:
        path = Path(__file__).with_name("custom_level.json")
        data = {"tiles": [[row, col] for row, col in sorted(self.editor_grid)]}
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.scene = "menu"

    def handle_event(self, event: pygame.event.Event, now: float) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        if self.scene == "menu":
            self.handle_menu(event)
        elif self.scene == "levels":
            self.handle_level_select(event)
        elif self.scene == "editor":
            self.handle_editor(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene = "menu"
        else:
            self.handle_game_event(event, now)
            if self.scene == "debug":
                self.handle_debug_panel(event, now)

    def draw(self, surface: pygame.Surface, now: float) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.scene == "menu":
            for button in self.menu_buttons:
                button.update(mouse_pos)
            self.draw_menu(surface)
        elif self.scene == "levels":
            self.draw_level_select(surface)
        elif self.scene == "editor":
            for button in self.editor_buttons:
                button.update(mouse_pos)
            self.draw_editor(surface)
        else:
            self.draw_game(surface, now)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Neon Breakout")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    while game.running:
        dt = min(clock.tick(FPS) / 1000.0, 0.033)
        now = pygame.time.get_ticks() / 1000.0
        for event in pygame.event.get():
            game.handle_event(event, now)
        game.update(dt, now, pygame.key.get_pressed())
        game.draw(screen, now)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
