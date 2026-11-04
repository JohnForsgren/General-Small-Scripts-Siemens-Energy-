"""Basic Breakout game built with Tkinter.

Controls:
- Left / Right arrows: move paddle
- Space: launch ball, or restart after win / loss
- Escape: quit
"""

from __future__ import annotations

import math
import random
import tkinter as tk
from collections.abc import Callable
from tkinter import ttk
from typing import TypedDict


HEIGHT = 600
FPS_DELAY_MS = 16

WIDTH = 1040
PADDLE_WIDTH = 110
PADDLE_HEIGHT = 14
PADDLE_Y = HEIGHT - 48
PADDLE_SPEED = 8

BALL_RADIUS = 8
BALL_SPEED = 5.6
MAX_BOUNCE_X = 4.8
MIN_BOUNCE_Y = 3.0
BALL_EFFECT_NORMAL = "normal"
BALL_EFFECT_RADIOACTIVE = "radioactive_ball"
BALL_EFFECT_ELECTRIC = "electric_ball"
BALL_ENHANCEMENT_DURATION_MS = 15_000
BALL_NORMAL_COLOR = "#f5f7fa"
BALL_RADIOACTIVE_COLOR = "#22c55e"
BALL_ELECTRIC_COLOR = "#facc15"

POWERUP_DROP_CHANCE = 0.15
POWERUP_SIZE = 18
POWERUP_SPEED = 2.6
POWERUP_TEXT_OFFSET = 20

LASER_POWER_DURATION_MS = 10_000
LASER_FIRE_INTERVAL_MS = 1_000
LASER_SPEED = 12
LASER_WIDTH = 4
LASER_HEIGHT = 18
BRICK_ELECTRIC_DURATION_MS = 5_000

PROBE_SIZE = 8
PROBE_SPEED = 4.2
PROBE_ORBIT_RADIUS = 24.0
PROBE_ORBIT_SPEED = 0.16
PROBE_ORBIT_STEP = PROBE_ORBIT_SPEED
PROBE_ORBIT_LOCK_DISTANCE = 18.0
PROBE_RADIUS = PROBE_SIZE / 2

POWERUP_LASER = "laser"
POWERUP_DOUBLE_BALL = "double_ball"
POWERUP_MULTIBALL = "multiball"
POWERUP_RADIOACTIVE = "radioactive_ball"
POWERUP_ELECTRIC = "electric_ball"
POWERUP_PROBE = "probe"
POWERUP_DWARF = "dwarf"
POWERUP_ALIEN = "alien"

DWARF_BODY_WIDTH = 18
DWARF_BODY_HEIGHT = 30
DWARF_PICKAXE_WIDTH = 22
DWARF_PICKAXE_HEIGHT = 10
DWARF_FLY_SPEED = 4.2
DWARF_CHARGE_MS = 2_000
DWARF_SPIN_SPEED = 0.22

ALIEN_BODY_SIZE = 16
ALIEN_FLY_SPEED = 4.6
ALIEN_INFECTION_DELAY_MS = 3_000
ALIEN_DESTROY_DELAY_MS = 5_000
ALIEN_COLOR = "#b197fc"
ALIEN_INFECT_COLOR = "#a855f7"
ALIEN_INFECT_DELAY_MS = ALIEN_INFECTION_DELAY_MS
ALIEN_INFECT_LIFETIME_MS = ALIEN_DESTROY_DELAY_MS

BRICK_UNIT = 16
BRICK_WIDTH = BRICK_UNIT * 4
BRICK_LAYER_OFFSET = BRICK_UNIT * 2
BRICK_ROWS = 6
BRICK_TOP = 72
BRICK_LEFT = 42
BRICK_GAP = 6
BRICK_HEIGHT = 22
BRICK_HEALTH_COLORS = {
    1: "#4dabf7",
    2: "#ffa94d",
    3: "#ff6b6b",
}

SPEED_MULTIPLIERS = (0.25, 0.5, 1.0, 1.5, 2.0)
MENU_BUTTON_WIDTH = 240
MENU_BUTTON_HEIGHT = 46
DEBUG_PANEL_WIDTH = 190
DEBUG_BUTTON_HEIGHT = 28

BG_COLOR = "#111722"
PADDLE_COLOR = "#7ee787"
BALL_COLOR = BALL_NORMAL_COLOR
POWERUP_COLOR = "#f5c542"
LASER_COLOR = "#5eead4"
DOUBLE_BALL_COLOR = "#8b5cf6"
MULTIBALL_COLOR = "#38bdf8"
RADIOACTIVE_POWERUP_COLOR = "#22c55e"
ELECTRIC_POWERUP_COLOR = "#facc15"
PROBE_COLOR = "#e2e8f0"
ELECTRIFIED_BRICK_COLOR = "#facc15"
ELECTRIFIED_COLOR = ELECTRIFIED_BRICK_COLOR
PROBE_OUTLINE_COLOR = "#64748b"
TEXT_COLOR = "#e6edf3"
SUBTLE_TEXT_COLOR = "#9fb0c3"
BRICK_COLORS = ("#ff6b6b", "#ffa94d", "#ffd43b", "#69db7c", "#4dabf7")
POWERUP_LABELS = {
    POWERUP_LASER: ("LASER", POWERUP_COLOR),
    POWERUP_DOUBLE_BALL: ("DOUBLE BALL", DOUBLE_BALL_COLOR),
    POWERUP_MULTIBALL: ("MULTIBALL", MULTIBALL_COLOR),
    POWERUP_RADIOACTIVE: ("RADIOACTIVE", RADIOACTIVE_POWERUP_COLOR),
    POWERUP_ELECTRIC: ("ELECTRIC", ELECTRIC_POWERUP_COLOR),
    POWERUP_PROBE: ("PROBE", PROBE_COLOR),
    POWERUP_DWARF: ("DWARF", "#f4a261"),
    POWERUP_ALIEN: ("ALIEN", "#b197fc"),
}
POWERUP_DROP_TYPES = tuple(POWERUP_LABELS.keys())
DEBUG_POWERUP_CHOICES = (
    "Random",
    "Laser",
    "Double Ball",
    "Multiball",
    "Radioactive Ball",
    "Electric Ball",
    "Probe",
    "Dwarf",
    "Alien",
)
DEBUG_POWERUP_TYPES = {
    "Random": None,
    "Laser": POWERUP_LASER,
    "Double Ball": POWERUP_DOUBLE_BALL,
    "Multiball": POWERUP_MULTIBALL,
    "Radioactive Ball": POWERUP_RADIOACTIVE,
    "Electric Ball": POWERUP_ELECTRIC,
    "Probe": POWERUP_PROBE,
    "Dwarf": POWERUP_DWARF,
    "Alien": POWERUP_ALIEN,
}

DEFAULT_SPEED_MULTIPLIER = 1.0


class ButtonSpec(TypedDict):
    rect: int
    text: int
    action: Callable[[], None]
    bounds: tuple[float, float, float, float]


class BallSpec(TypedDict):
    id: int
    dx: float
    dy: float
    attached: bool
    enhancement: str
    enhancement_until_ms: int


class PowerupSpec(TypedDict):
    shape: int
    label: int
    type: str


class BrickSpec(TypedDict):
    health: int
    electrified_until_ms: int
    electrified: bool
    row: int
    column: int


class ProbeSpec(TypedDict):
    id: int
    state: str
    target_ball_id: int
    angle: float
    orbit_radius: float


class SpecialPowerupSpec(TypedDict):
    type: str
    body_id: int
    aux_id: int
    state: str
    target_brick_id: int
    activated_ms: int
    latch_until_ms: int
    orbit_angle: float
    body_vy: float


class AlienInfectionSpec(TypedDict):
    brick_id: int
    infected_ms: int
    destroy_ms: int
    spread_done: bool


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


class BreakoutGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Breakout")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        self.canvas = tk.Canvas(
            self.root,
            width=WIDTH,
            height=HEIGHT,
            bg=BG_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.left_pressed = False
        self.right_pressed = False
        self.screen = "menu"
        self.mode = "main"
        self.state = "ready"
        self.score = 0
        self.lives = 3
        self.bricks_remaining = 0
        self.paddle_x = WIDTH / 2
        self.speed_multiplier = DEFAULT_SPEED_MULTIPLIER
        self.debug_brick_tool_enabled = False
        self.debug_brick_painting = False
        self.debug_brick_destroy_tool_enabled = False
        self.debug_brick_destroying = False
        self.debug_brick_health = 1
        self.debug_drop_powerup_var = tk.StringVar(value="Random")
        self.balls: list[BallSpec] = []
        self.special_powerups: list[SpecialPowerupSpec] = []
        self.alien_infections: dict[int, AlienInfectionSpec] = {}
        self.clock_ms = 0
        self.laser_until_ms = 0
        self.last_laser_fire_ms = -LASER_FIRE_INTERVAL_MS
        self.powerups: list[PowerupSpec] = []
        self.probes: list[ProbeSpec] = []
        self.lasers: list[int] = []
        self.bricks_by_id: dict[int, BrickSpec] = {}
        self.menu_buttons: list[ButtonSpec] = []
        self.debug_buttons: list[ButtonSpec] = []
        self.debug_drop_combo: ttk.Combobox | None = None
        self.debug_destroy_button: ttk.Button | None = None
        self.debug_drop_combo_id: int | None = None
        self.debug_destroy_button_id: int | None = None

        self.status_id = self.canvas.create_text(
            16,
            12,
            anchor="nw",
            fill=TEXT_COLOR,
            font=("Segoe UI", 14, "bold"),
            text="",
        )
        self.help_id = self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2,
            fill=TEXT_COLOR,
            font=("Segoe UI", 20, "bold"),
            text="",
        )
        self.subtext_id = self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2 + 36,
            fill=SUBTLE_TEXT_COLOR,
            font=("Segoe UI", 11),
            text="Left/Right to move, Space to launch",
        )

        self.paddle_id = self.canvas.create_rectangle(0, 0, 0, 0, fill=PADDLE_COLOR, outline=PADDLE_COLOR)

        self.bind_controls()
        self.show_menu()
        self.root.after(FPS_DELAY_MS, self.tick)

    def bind_controls(self) -> None:
        self.root.bind_all("<KeyPress-Left>", lambda _event: self.set_left_pressed(True))
        self.root.bind_all("<KeyRelease-Left>", lambda _event: self.set_left_pressed(False))
        self.root.bind_all("<KeyPress-Right>", lambda _event: self.set_right_pressed(True))
        self.root.bind_all("<KeyRelease-Right>", lambda _event: self.set_right_pressed(False))
        self.root.bind_all("<KeyPress-space>", self.handle_space)
        self.root.bind_all("<space>", self.handle_space)
        self.root.bind_all("<KeyPress-Escape>", self.handle_escape)
        self.root.bind_all("<KeyPress-1>", lambda _event: self.set_debug_speed(0.25))
        self.root.bind_all("<KeyPress-2>", lambda _event: self.set_debug_speed(0.5))
        self.root.bind_all("<KeyPress-3>", lambda _event: self.set_debug_speed(1.0))
        self.root.bind_all("<KeyPress-4>", lambda _event: self.set_debug_speed(1.5))
        self.root.bind_all("<KeyPress-5>", lambda _event: self.set_debug_speed(2.0))
        self.root.bind_all("<KeyPress-b>", lambda _event: self.toggle_debug_brick_tool())
        self.root.bind_all("<KeyPress-B>", lambda _event: self.toggle_debug_brick_tool())
        self.canvas.bind("<Button-1>", lambda _event: self.root.focus_force())
        self.canvas.bind("<ButtonPress-1>", self.handle_canvas_press)
        self.canvas.bind("<B1-Motion>", self.handle_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.handle_canvas_release)
        self.root.after(100, self.root.focus_force)

    def set_left_pressed(self, pressed: bool) -> None:
        self.left_pressed = pressed

    def set_right_pressed(self, pressed: bool) -> None:
        self.right_pressed = pressed

    def handle_escape(self, _event: tk.Event | None = None) -> None:
        if self.screen == "menu":
            self.root.destroy()
        else:
            self.show_menu()

    def set_debug_speed(self, multiplier: float) -> None:
        if self.mode == "debug":
            self.speed_multiplier = multiplier

    def toggle_debug_brick_tool(self) -> None:
        if self.mode != "debug":
            return

        self.debug_brick_tool_enabled = not self.debug_brick_tool_enabled
        self.debug_brick_painting = False

    def destroy_random_debug_brick(self) -> None:
        if self.screen != "game" or self.mode != "debug" or not self.bricks_by_id:
            return

        brick_id = random.choice(list(self.bricks_by_id.keys()))
        self.destroy_brick(brick_id, drop_powerup=True, force_drop_powerup=True, forced_powerup_type=self.debug_powerup_type())
        self.root.focus_force()

    def start_game(self, mode: str) -> None:
        self.mode = mode
        self.screen = "game"
        self.canvas.delete("ui")
        self.canvas.delete("menu")
        self.speed_multiplier = DEFAULT_SPEED_MULTIPLIER
        self.debug_brick_tool_enabled = False
        self.debug_brick_painting = False
        self.debug_brick_destroy_tool_enabled = False
        self.debug_brick_destroying = False
        self.debug_drop_powerup_var.set("Random")
        self.create_game_scene()
        self.reset_game()

    def create_game_scene(self) -> None:
        self.status_id = self.canvas.create_text(
            16,
            12,
            anchor="nw",
            fill=TEXT_COLOR,
            font=("Segoe UI", 14, "bold"),
            text="",
        )
        self.help_id = self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2,
            fill=TEXT_COLOR,
            font=("Segoe UI", 20, "bold"),
            text="",
        )
        self.subtext_id = self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2 + 36,
            fill=SUBTLE_TEXT_COLOR,
            font=("Segoe UI", 11),
            text="Left/Right to move, Space to launch",
        )
        self.paddle_id = self.canvas.create_rectangle(0, 0, 0, 0, fill=PADDLE_COLOR, outline=PADDLE_COLOR)

        if self.mode == "debug":
            self.create_debug_drop_controls()

        if self.mode == "debug":
            self.create_debug_drop_controls()

    def show_menu(self) -> None:
        self.screen = "menu"
        self.mode = "main"
        self.canvas.delete("all")
        self.menu_buttons = []

        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=BG_COLOR, outline=BG_COLOR, tags=("menu",))
        self.canvas.create_text(
            WIDTH / 2,
            110,
            text="Breakout",
            fill=TEXT_COLOR,
            font=("Segoe UI", 32, "bold"),
            tags=("menu",),
        )
        self.canvas.create_text(
            WIDTH / 2,
            160,
            text="Choose a mode",
            fill=SUBTLE_TEXT_COLOR,
            font=("Segoe UI", 13),
            tags=("menu",),
        )

        self.create_menu_button(WIDTH / 2, 250, "Main Game", lambda: self.start_game("main"))
        self.create_menu_button(WIDTH / 2, 316, "Debug Mode", lambda: self.start_game("debug"))

        self.canvas.create_text(
            WIDTH / 2,
            420,
            text="Escape quits from the menu.",
            fill=SUBTLE_TEXT_COLOR,
            font=("Segoe UI", 10),
            tags=("menu",),
        )

    def create_menu_button(self, center_x: float, center_y: float, label: str, action: Callable[[], None]) -> None:
        left = center_x - MENU_BUTTON_WIDTH / 2
        top = center_y - MENU_BUTTON_HEIGHT / 2
        right = center_x + MENU_BUTTON_WIDTH / 2
        bottom = center_y + MENU_BUTTON_HEIGHT / 2
        rect_id = self.canvas.create_rectangle(left, top, right, bottom, fill="#1f2a3a", outline="#3b4b62", width=2, tags=("menu",))
        text_id = self.canvas.create_text(center_x, center_y, text=label, fill=TEXT_COLOR, font=("Segoe UI", 14, "bold"), tags=("menu",))
        self.menu_buttons.append({"rect": rect_id, "text": text_id, "action": action, "bounds": (left, top, right, bottom)})

    def handle_canvas_press(self, event: tk.Event) -> None:
        if self.screen == "menu":
            self.handle_menu_click(event.x, event.y)
            return

        if self.mode == "debug":
            if self.handle_debug_ui_click(event.x, event.y):
                return
            if self.handle_debug_powerup_click(event.x, event.y):
                return
            if self.debug_brick_tool_enabled:
                self.debug_brick_painting = True
                self.place_debug_brick(event.x, event.y)

    def handle_canvas_drag(self, event: tk.Event) -> None:
        if self.screen == "game" and self.mode == "debug" and self.debug_brick_tool_enabled and self.debug_brick_painting:
            self.place_debug_brick(event.x, event.y)

    def handle_canvas_release(self, _event: tk.Event) -> None:
        self.debug_brick_painting = False

    def handle_menu_click(self, x: float, y: float) -> None:
        for button in self.menu_buttons:
            left, top, right, bottom = button["bounds"]
            if left <= x <= right and top <= y <= bottom:
                action = button["action"]
                action()
                break

    def handle_debug_ui_click(self, x: float, y: float) -> bool:
        for button in self.debug_buttons:
            left, top, right, bottom = button["bounds"]
            if left <= x <= right and top <= y <= bottom:
                action = button["action"]
                action()
                return True

        return False

    def create_debug_drop_controls(self) -> None:
        if self.debug_drop_combo_id is not None:
            self.canvas.delete(self.debug_drop_combo_id)
            self.debug_drop_combo_id = None
        if self.debug_destroy_button_id is not None:
            self.canvas.delete(self.debug_destroy_button_id)
            self.debug_destroy_button_id = None

        panel_left = WIDTH - DEBUG_PANEL_WIDTH + 12
        self.canvas.create_text(
            panel_left,
            500,
            anchor="nw",
            text="Drop Powerup",
            fill=TEXT_COLOR,
            font=("Segoe UI", 9, "bold"),
            tags=("ui",),
        )
        self.debug_drop_combo = ttk.Combobox(self.root, textvariable=self.debug_drop_powerup_var, values=DEBUG_POWERUP_CHOICES, state="readonly", width=15, takefocus=False)
        self.debug_drop_combo_id = self.canvas.create_window(panel_left, 518, anchor="nw", window=self.debug_drop_combo)
        self.debug_destroy_button = ttk.Button(self.root, text="Destroy Brick", command=self.destroy_random_debug_brick, takefocus=False)
        self.debug_destroy_button_id = self.canvas.create_window(panel_left, 552, anchor="nw", width=DEBUG_PANEL_WIDTH - 24, window=self.debug_destroy_button)

    def debug_powerup_type(self) -> str | None:
        return DEBUG_POWERUP_TYPES.get(self.debug_drop_powerup_var.get(), None)

    def debug_brick_slot_at(self, x: float, y: float) -> tuple[float, float, int, int] | None:
        playfield_width = self.gameplay_width()
        if x < BRICK_LEFT or x > playfield_width - BRICK_LEFT:
            return None
        if y < BRICK_TOP:
            return None

        row_span = BRICK_HEIGHT + BRICK_GAP
        row = int((y - BRICK_TOP) // row_span)
        if row < 0 or row >= BRICK_ROWS:
            return None

        row_top = BRICK_TOP + row * row_span
        row_y_offset = y - row_top
        if row_y_offset < 0 or row_y_offset > BRICK_HEIGHT:
            return None

        row_offset = (row % 2) * BRICK_LAYER_OFFSET
        row_left = BRICK_LEFT - row_offset
        col_span = BRICK_WIDTH + BRICK_GAP
        column = int((x - row_left) // col_span)
        if column < 0:
            return None

        column_left = row_left + column * col_span
        if x < column_left or x > column_left + BRICK_WIDTH:
            return None

        if column_left < 0 or column_left + BRICK_WIDTH > playfield_width:
            return None

        return column_left, row_top, row, column

    def brick_at_slot(self, row: int, column: int) -> int | None:
        for item_id, brick in self.bricks_by_id.items():
            if brick["row"] == row and brick["column"] == column:
                return item_id

        return None

    def handle_debug_powerup_click(self, x: float, y: float) -> bool:
        for powerup in self.powerups[:]:
            shape_id = int(powerup["shape"])
            label_id = int(powerup["label"])
            shape_coords = self.canvas.bbox(shape_id)
            label_coords = self.canvas.bbox(label_id)
            if (shape_coords and shape_coords[0] <= x <= shape_coords[2] and shape_coords[1] <= y <= shape_coords[3]) or (
                label_coords and label_coords[0] <= x <= label_coords[2] and label_coords[1] <= y <= label_coords[3]
            ):
                self.canvas.delete(shape_id)
                self.canvas.delete(label_id)
                self.powerups.remove(powerup)
                self.apply_powerup_effect(powerup["type"])
                return True

        return False

    def place_debug_brick(self, x: float, y: float) -> None:
        if self.screen != "game" or self.mode != "debug":
            return

        slot = self.debug_brick_slot_at(x, y)
        if slot is None:
            return

        left, top, row, column = slot
        if self.brick_at_slot(row, column) is not None:
            return

        self.create_brick(left, top, self.debug_brick_health, row, column)

    def destroy_debug_brick(self, x: float, y: float) -> bool:
        if self.screen != "game" or self.mode != "debug":
            return False

        slot = self.debug_brick_slot_at(x, y)
        if slot is None:
            return False

        _left, _top, row, column = slot
        brick_id = self.brick_at_slot(row, column)
        if brick_id is None:
            return False

        self.destroy_brick(brick_id, drop_powerup=True, force_drop_powerup=True, forced_powerup_type=self.debug_powerup_type())
        return True

    def draw_debug_panel(self) -> None:
        self.canvas.delete("ui")
        self.debug_buttons = []

        panel_left = WIDTH - DEBUG_PANEL_WIDTH
        self.canvas.create_rectangle(panel_left, 0, WIDTH, HEIGHT, fill="#182130", outline="#263246", tags=("ui",))
        self.canvas.create_text(
            panel_left + DEBUG_PANEL_WIDTH / 2,
            26,
            text="Debug",
            fill=TEXT_COLOR,
            font=("Segoe UI", 16, "bold"),
            tags=("ui",),
        )
        self.canvas.create_text(
            panel_left + 12,
            56,
            anchor="nw",
            text="Click powerups to auto-collect.",
            fill=SUBTLE_TEXT_COLOR,
            font=("Segoe UI", 9),
            tags=("ui",),
        )

        self.create_debug_button(panel_left + 12, 88, DEBUG_PANEL_WIDTH - 24, DEBUG_BUTTON_HEIGHT, f"Brick Tool: {'ON' if self.debug_brick_tool_enabled else 'OFF'}", self.toggle_debug_brick_tool)
        self.canvas.create_text(
            panel_left + 12,
            126,
            anchor="nw",
            text=f"Brick Health: {self.debug_brick_health}",
            fill=TEXT_COLOR,
            font=("Segoe UI", 10, "bold"),
            tags=("ui",),
        )

        health_y = 150
        for health in (1, 2, 3):
            self.create_debug_button(
                panel_left + 12,
                health_y,
                48,
                DEBUG_BUTTON_HEIGHT,
                str(health),
                lambda value=health: self.set_debug_brick_health(value),
            )
            health_y += 34

        self.canvas.create_text(
            panel_left + 12,
            260,
            anchor="nw",
            text="Speed",
            fill=TEXT_COLOR,
            font=("Segoe UI", 10, "bold"),
            tags=("ui",),
        )
        speed_y = 286
        for multiplier in SPEED_MULTIPLIERS:
            self.create_debug_button(
                panel_left + 12,
                speed_y,
                DEBUG_PANEL_WIDTH - 24,
                DEBUG_BUTTON_HEIGHT,
                f"x{multiplier:g}",
                lambda value=multiplier: self.set_debug_speed(value),
            )
            speed_y += 34

        self.canvas.create_text(
            panel_left + 12,
            470,
            anchor="nw",
            text="Press Esc to menu",
            fill=SUBTLE_TEXT_COLOR,
            font=("Segoe UI", 9),
            tags=("ui",),
        )

    def create_debug_button(self, x: float, y: float, width: float, height: float, label: str, action: Callable[[], None]) -> None:
        rect_id = self.canvas.create_rectangle(x, y, x + width, y + height, fill="#233047", outline="#3c4c67", tags=("ui",))
        text_id = self.canvas.create_text(x + width / 2, y + height / 2, text=label, fill=TEXT_COLOR, font=("Segoe UI", 9, "bold"), tags=("ui",))
        self.debug_buttons.append({"rect": rect_id, "text": text_id, "action": action, "bounds": (x, y, x + width, y + height)})

    def set_debug_brick_health(self, health: int) -> None:
        if self.mode == "debug":
            self.debug_brick_health = health

    def ball_color_for_enhancement(self, enhancement: str) -> str:
        if enhancement == BALL_EFFECT_RADIOACTIVE:
            return BALL_RADIOACTIVE_COLOR
        if enhancement == BALL_EFFECT_ELECTRIC:
            return BALL_ELECTRIC_COLOR
        return BALL_NORMAL_COLOR

    def add_attached_ball(self, enhancement: str = BALL_EFFECT_NORMAL) -> None:
        ball_id = self.canvas.create_oval(0, 0, 0, 0, fill=self.ball_color_for_enhancement(enhancement), outline=self.ball_color_for_enhancement(enhancement), tags=("ball",))
        self.balls.append(
            {
                "id": ball_id,
                "dx": 0.0,
                "dy": 0.0,
                "attached": True,
                "enhancement": enhancement,
                "enhancement_until_ms": 0,
            }
        )

    def position_attached_balls(self) -> None:
        attached_balls = [ball for ball in self.balls if ball["attached"]]
        if not attached_balls:
            return

        spacing = BALL_RADIUS * 2 + 6
        start_x = self.paddle_x - spacing * (len(attached_balls) - 1) / 2
        ball_y = PADDLE_Y - BALL_RADIUS * 2 - 4

        for index, ball in enumerate(attached_balls):
            ball_x = start_x + index * spacing
            ball_id = int(ball["id"])
            ball["dx"] = 0.0
            ball["dy"] = 0.0
            ball_left = ball_x - BALL_RADIUS
            ball_top = ball_y
            ball_right = ball_x + BALL_RADIUS
            ball_bottom = ball_y + BALL_RADIUS * 2
            self.canvas.coords(ball_id, ball_left, ball_top, ball_right, ball_bottom)

    def set_ball_enhancement(self, ball: BallSpec, enhancement: str) -> None:
        ball["enhancement"] = enhancement
        if enhancement == BALL_EFFECT_NORMAL:
            ball["enhancement_until_ms"] = 0
        else:
            ball["enhancement_until_ms"] = self.clock_ms + BALL_ENHANCEMENT_DURATION_MS

        ball_id = int(ball["id"])
        color = self.ball_color_for_enhancement(enhancement)
        self.canvas.itemconfig(ball_id, fill=color, outline=color)

    def update_ball_enhancements(self) -> None:
        for ball in self.balls:
            if ball["enhancement"] == BALL_EFFECT_NORMAL:
                continue

            if self.clock_ms < ball["enhancement_until_ms"]:
                continue

            self.set_ball_enhancement(ball, BALL_EFFECT_NORMAL)

    def select_ball_for_enhancement(self) -> BallSpec | None:
        candidates = [ball for ball in self.balls if ball["enhancement"] == BALL_EFFECT_NORMAL]
        if not candidates:
            return None

        return random.choice(candidates)

    def enhance_random_ball(self, enhancement: str) -> None:
        ball = self.select_ball_for_enhancement()
        if ball is None:
            return

        self.set_ball_enhancement(ball, enhancement)

    def spawn_probe(self) -> None:
        probe_x = self.paddle_x
        probe_y = PADDLE_Y - 26
        probe_id = self.canvas.create_oval(
            probe_x - PROBE_RADIUS,
            probe_y - PROBE_RADIUS,
            probe_x + PROBE_RADIUS,
            probe_y + PROBE_RADIUS,
            fill=PROBE_COLOR,
            outline=PROBE_OUTLINE_COLOR,
            tags=("probe",),
        )
        target_ball_id = self.nearest_ball_id(probe_x, probe_y)
        self.probes.append(
            {
                "id": probe_id,
                "state": "fly",
                "target_ball_id": target_ball_id,
                "angle": 0.0,
                "orbit_radius": PROBE_ORBIT_RADIUS,
            }
        )

    def nearest_ball_id(self, x: float, y: float) -> int:
        best_ball_id = -1
        best_distance = float("inf")
        for ball in self.balls:
            ball_id = int(ball["id"])
            coords = self.canvas.coords(ball_id)
            if len(coords) != 4:
                continue

            center_x = (coords[0] + coords[2]) / 2
            center_y = (coords[1] + coords[3]) / 2
            distance = math.hypot(center_x - x, center_y - y)
            if distance < best_distance:
                best_distance = distance
                best_ball_id = ball_id

        return best_ball_id

    def gameplay_width(self) -> float:
        if self.screen == "game" and self.mode == "debug":
            return WIDTH - DEBUG_PANEL_WIDTH

        return WIDTH

    def reset_game(self) -> None:
        self.canvas.delete("brick")
        self.canvas.delete("powerup")
        self.canvas.delete("laser")
        self.canvas.delete("ball")
        self.canvas.delete("probe")
        self.canvas.delete("special")
        self.score = 0
        self.lives = 3
        self.state = "ready"
        self.clock_ms = 0
        self.laser_until_ms = 0
        self.last_laser_fire_ms = -LASER_FIRE_INTERVAL_MS
        self.powerups.clear()
        self.lasers.clear()
        self.balls.clear()
        self.special_powerups.clear()
        self.alien_infections.clear()
        self.probes.clear()
        self.bricks_by_id.clear()
        self.paddle_x = self.gameplay_width() / 2
        self.create_bricks()
        self.place_paddle()
        self.add_attached_ball()
        self.position_attached_balls()
        self.refresh_hud()
        self.refresh_message()

    def create_bricks(self) -> None:
        self.bricks_remaining = 0
        playfield_right = self.gameplay_width()
        for row in range(BRICK_ROWS):
            health = (row % 3) + 1
            y1 = BRICK_TOP + row * (BRICK_HEIGHT + BRICK_GAP)
            row_offset = (row % 2) * BRICK_LAYER_OFFSET
            x = BRICK_LEFT - row_offset
            max_x = playfield_right - BRICK_LEFT + row_offset
            column = 0

            while x + BRICK_WIDTH <= max_x:
                self.create_brick(x, y1, health, row, column)
                x += BRICK_WIDTH
                column += 1

    def create_brick(self, x1: float, y1: float, health: int, row: int = -1, column: int = -1) -> int:
        color = BRICK_HEALTH_COLORS[health]
        x2 = x1 + BRICK_WIDTH
        y2 = y1 + BRICK_HEIGHT
        brick_id = self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=color,
            outline=BG_COLOR,
            tags=("brick",),
        )
        self.bricks_by_id[brick_id] = {
            "health": health,
            "electrified_until_ms": 0,
            "electrified": False,
            "row": row,
            "column": column,
        }
        self.bricks_remaining += 1
        return brick_id

    def place_paddle(self) -> None:
        half_width = PADDLE_WIDTH / 2
        left = self.paddle_x - half_width
        right = self.paddle_x + half_width
        top = PADDLE_Y
        bottom = PADDLE_Y + PADDLE_HEIGHT
        self.canvas.coords(self.paddle_id, left, top, right, bottom)

    def attach_ball_to_paddle(self) -> None:
        self.balls = []
        self.add_attached_ball()
        self.position_attached_balls()

    def spawn_ball(self, center_x: float, center_y: float, ball_dx: float, ball_dy: float, attached: bool = False, enhancement: str = BALL_EFFECT_NORMAL) -> int:
        color = self.ball_color_for_enhancement(enhancement)
        ball_id = self.canvas.create_oval(0, 0, 0, 0, fill=color, outline=color, tags=("ball",))
        ball_left = center_x - BALL_RADIUS
        ball_top = center_y - BALL_RADIUS
        ball_right = center_x + BALL_RADIUS
        ball_bottom = center_y + BALL_RADIUS
        self.canvas.coords(ball_id, ball_left, ball_top, ball_right, ball_bottom)
        self.balls.append(
            {
                "id": ball_id,
                "dx": ball_dx,
                "dy": ball_dy,
                "attached": attached,
                "enhancement": enhancement,
                "enhancement_until_ms": 0,
            }
        )
        return ball_id

    def active_balls(self) -> list[BallSpec]:
        return [ball for ball in self.balls if not ball["attached"]]

    def launch_ball(self) -> None:
        direction = 1 if self.paddle_x >= self.gameplay_width() / 2 else -1
        for ball in self.balls:
            if ball["attached"]:
                ball["attached"] = False
                ball["dx"] = 2.8 * direction
                ball["dy"] = -4.8
        for powerup in self.special_powerups:
            if powerup["state"] == "held":
                powerup["state"] = "flight"
                powerup["activated_ms"] = self.clock_ms
                powerup["body_vy"] = -DWARF_FLY_SPEED if powerup["type"] == POWERUP_DWARF else -ALIEN_FLY_SPEED
        self.state = "playing"
        self.refresh_message()

    def sync_attached_ball_to_paddle(self) -> None:
        if not self.balls:
            self.add_attached_ball()

        if not self.active_balls():
            self.position_attached_balls()

    def ball_coords(self, ball: BallSpec) -> tuple[float, float, float, float]:
        ball_id = int(ball["id"])
        coords = self.canvas.coords(ball_id)
        if len(coords) != 4:
            return (0.0, 0.0, 0.0, 0.0)
        return coords[0], coords[1], coords[2], coords[3]

    def get_ball_by_id(self, ball_id: int) -> BallSpec | None:
        for ball in self.balls:
            if int(ball["id"]) == ball_id:
                return ball

        return None

    def spawn_copy_from_ball(self, source_ball: BallSpec) -> None:
        left, top, right, bottom = self.ball_coords(source_ball)
        center_x = (left + right) / 2
        center_y = (top + bottom) / 2
        source_dx = float(source_ball["dx"])
        source_dy = float(source_ball["dy"])
        source_effect = source_ball["enhancement"]

        copy_dx = -source_dx if abs(source_dx) >= 0.8 else random.choice((-2.6, 2.6))
        copy_dy = source_dy if abs(source_dy) >= 0.8 else -4.6
        self.spawn_ball(center_x, center_y, copy_dx, copy_dy, attached=False, enhancement=source_effect)

    def add_double_ball(self) -> None:
        active_balls = self.active_balls()
        if active_balls:
            self.spawn_copy_from_ball(random.choice(active_balls))
            return

        attached_balls = [ball for ball in self.balls if ball["attached"]]
        if attached_balls:
            self.spawn_copy_from_ball(random.choice(attached_balls))
            return

        self.spawn_ball(self.paddle_x, PADDLE_Y - BALL_RADIUS * 2 - 4, random.choice((-2.6, 2.6)), -4.6, attached=False)

    def add_multiball(self) -> None:
        self.add_attached_ball()
        self.position_attached_balls()

    def apply_powerup_effect(self, powerup_type: str) -> None:
        if powerup_type == POWERUP_LASER:
            self.activate_laser()
        elif powerup_type == POWERUP_DOUBLE_BALL:
            self.add_double_ball()
        elif powerup_type == POWERUP_MULTIBALL:
            self.add_multiball()
        elif powerup_type == POWERUP_RADIOACTIVE:
            self.enhance_random_ball(BALL_EFFECT_RADIOACTIVE)
        elif powerup_type == POWERUP_ELECTRIC:
            self.enhance_random_ball(BALL_EFFECT_ELECTRIC)
        elif powerup_type == POWERUP_PROBE:
            self.spawn_probe()
        elif powerup_type == POWERUP_DWARF:
            self.spawn_dwarf()
        elif powerup_type == POWERUP_ALIEN:
            self.spawn_alien()

    def rotated_rectangle_points(self, center_x: float, center_y: float, width: float, height: float, angle: float) -> tuple[float, ...]:
        half_width = width / 2
        half_height = height / 2
        sin_angle = math.sin(angle)
        cos_angle = math.cos(angle)
        corners = [(-half_width, -half_height), (half_width, -half_height), (half_width, half_height), (-half_width, half_height)]
        points: list[float] = []
        for x_offset, y_offset in corners:
            rotated_x = center_x + x_offset * cos_angle - y_offset * sin_angle
            rotated_y = center_y + x_offset * sin_angle + y_offset * cos_angle
            points.extend((rotated_x, rotated_y))

        return tuple(points)

    def spawn_dwarf(self) -> None:
        body_left = self.paddle_x - DWARF_BODY_WIDTH / 2
        body_top = PADDLE_Y - DWARF_BODY_HEIGHT - 6
        body_right = self.paddle_x + DWARF_BODY_WIDTH / 2
        body_bottom = PADDLE_Y - 6
        body_id = self.canvas.create_rectangle(body_left, body_top, body_right, body_bottom, fill="#f4a261", outline="#f97316", tags=("special",))
        pickaxe_id = self.canvas.create_polygon(0, 0, 0, 0, fill="#cbd5e1", outline="#94a3b8", tags=("special",))
        self.canvas.itemconfigure(pickaxe_id, state="hidden")
        self.special_powerups.append(
            {
                "type": POWERUP_DWARF,
                "body_id": body_id,
                "aux_id": pickaxe_id,
                "state": "held",
                "target_brick_id": -1,
                "activated_ms": 0,
                "latch_until_ms": 0,
                "orbit_angle": 0.0,
                "body_vy": 0.0,
            }
        )

    def spawn_alien(self) -> None:
        body_left = self.paddle_x - ALIEN_BODY_SIZE / 2
        body_top = PADDLE_Y - ALIEN_BODY_SIZE - 8
        body_right = self.paddle_x + ALIEN_BODY_SIZE / 2
        body_bottom = PADDLE_Y - 8
        body_id = self.canvas.create_oval(body_left, body_top, body_right, body_bottom, fill=ALIEN_COLOR, outline=ALIEN_COLOR, tags=("special",))
        aux_id = self.canvas.create_oval(body_left - 4, body_top - 4, body_right + 4, body_bottom + 4, outline=ALIEN_INFECT_COLOR, width=2, tags=("special",))
        self.canvas.itemconfigure(aux_id, state="hidden")
        self.special_powerups.append(
            {
                "type": POWERUP_ALIEN,
                "body_id": body_id,
                "aux_id": aux_id,
                "state": "held",
                "target_brick_id": -1,
                "activated_ms": 0,
                "latch_until_ms": 0,
                "orbit_angle": 0.0,
                "body_vy": 0.0,
            }
        )

    def place_special_powerup_on_paddle(self, powerup: SpecialPowerupSpec) -> None:
        body_id = int(powerup["body_id"])
        aux_id = int(powerup["aux_id"])
        if powerup["type"] == POWERUP_DWARF:
            left = self.paddle_x - DWARF_BODY_WIDTH / 2
            top = PADDLE_Y - DWARF_BODY_HEIGHT - 6
            right = self.paddle_x + DWARF_BODY_WIDTH / 2
            bottom = PADDLE_Y - 6
            self.canvas.coords(body_id, left, top, right, bottom)
            self.canvas.itemconfigure(aux_id, state="hidden")
        else:
            left = self.paddle_x - ALIEN_BODY_SIZE / 2
            top = PADDLE_Y - ALIEN_BODY_SIZE - 8
            right = self.paddle_x + ALIEN_BODY_SIZE / 2
            bottom = PADDLE_Y - 8
            self.canvas.coords(body_id, left, top, right, bottom)
            self.canvas.coords(aux_id, left - 4, top - 4, right + 4, bottom + 4)
            self.canvas.itemconfigure(aux_id, state="hidden")

    def remove_special_powerup(self, powerup: SpecialPowerupSpec) -> None:
        self.canvas.delete(int(powerup["body_id"]))
        self.canvas.delete(int(powerup["aux_id"]))
        if powerup in self.special_powerups:
            self.special_powerups.remove(powerup)

    def queue_alien_infection(self, brick_id: int, infected_ms: int | None = None) -> None:
        if brick_id not in self.bricks_by_id or brick_id in self.alien_infections:
            return

        if infected_ms is None:
            infected_ms = self.clock_ms + ALIEN_INFECT_DELAY_MS

        infection: AlienInfectionSpec = {
            "brick_id": brick_id,
            "infected_ms": infected_ms,
            "destroy_ms": infected_ms + ALIEN_INFECT_LIFETIME_MS,
            "spread_done": False,
        }
        self.alien_infections[brick_id] = infection

    def spread_alien_infection(self, brick_id: int) -> None:
        coords = self.canvas.coords(brick_id)
        if len(coords) != 4:
            return

        x1, y1, x2, y2 = coords
        center_y = (y1 + y2) / 2
        hits = self.canvas.find_overlapping(x1 - BRICK_WIDTH / 2, y1 - BRICK_HEIGHT, x2 + BRICK_WIDTH / 2, y1 + 1)
        for hit_id in hits:
            if hit_id == brick_id or hit_id not in self.bricks_by_id:
                continue

            hit_coords = self.canvas.coords(hit_id)
            if len(hit_coords) != 4:
                continue

            hit_center_y = (hit_coords[1] + hit_coords[3]) / 2
            if hit_center_y >= center_y:
                continue

            self.queue_alien_infection(hit_id)

    def update_alien_infections(self) -> None:
        for brick_id, infection in list(self.alien_infections.items()):
            brick = self.bricks_by_id.get(brick_id)
            if brick is None:
                self.alien_infections.pop(brick_id, None)
                continue

            if self.clock_ms < infection["infected_ms"]:
                continue

            if not infection["spread_done"]:
                self.canvas.itemconfig(brick_id, fill=ALIEN_INFECT_COLOR, outline=ALIEN_INFECT_COLOR)
                self.spread_alien_infection(brick_id)
                infection["spread_done"] = True

            if self.clock_ms >= infection["destroy_ms"]:
                self.alien_infections.pop(brick_id, None)
                self.destroy_brick(brick_id)

    def update_special_powerups(self) -> None:
        for powerup in self.special_powerups[:]:
            body_id = int(powerup["body_id"])
            aux_id = int(powerup["aux_id"])
            body_coords = self.canvas.coords(body_id)
            if len(body_coords) != 4:
                self.remove_special_powerup(powerup)
                continue

            if powerup["state"] == "held":
                self.place_special_powerup_on_paddle(powerup)
                continue

            if powerup["type"] == POWERUP_DWARF:
                self.canvas.itemconfigure(aux_id, state="normal")
                if powerup["state"] == "flight":
                    self.canvas.move(body_id, 0, powerup["body_vy"])
                    self.canvas.move(aux_id, 0, powerup["body_vy"])
                    body_coords = self.canvas.coords(body_id)
                    if len(body_coords) != 4:
                        self.remove_special_powerup(powerup)
                        continue

                    hits = self.canvas.find_overlapping(*body_coords)
                    for hit_id in hits:
                        if hit_id in self.bricks_by_id:
                            powerup["state"] = "charge"
                            powerup["target_brick_id"] = hit_id
                            powerup["activated_ms"] = self.clock_ms + DWARF_CHARGE_MS
                            powerup["orbit_angle"] = 0.0
                            powerup["body_vy"] = 0.0
                            self.canvas.coords(body_id, *body_coords)
                            break
                elif powerup["state"] == "charge":
                    if self.clock_ms >= powerup["activated_ms"]:
                        powerup["state"] = "orbit"
                        powerup["orbit_angle"] = 0.0
                elif powerup["state"] == "orbit":
                    self.canvas.move(body_id, 0, -1.4)
                    self.canvas.move(aux_id, 0, -1.4)
                    body_coords = self.canvas.coords(body_id)
                    if len(body_coords) != 4 or body_coords[3] <= 0:
                        self.remove_special_powerup(powerup)
                        continue

                    body_left, body_top, body_right, body_bottom = body_coords
                    body_center_x = (body_left + body_right) / 2
                    shoulder_x = body_center_x
                    shoulder_y = body_top + DWARF_BODY_HEIGHT * 0.72
                    powerup["orbit_angle"] += DWARF_SPIN_SPEED
                    pickaxe_center_x = shoulder_x + math.cos(powerup["orbit_angle"]) * 14
                    pickaxe_center_y = shoulder_y + math.sin(powerup["orbit_angle"]) * 14
                    points = self.rotated_rectangle_points(pickaxe_center_x, pickaxe_center_y, DWARF_PICKAXE_WIDTH, DWARF_PICKAXE_HEIGHT, powerup["orbit_angle"] + math.pi / 2)
                    self.canvas.coords(aux_id, *points)

                    hits = self.canvas.find_overlapping(*self.canvas.bbox(aux_id))
                    for hit_id in hits:
                        if hit_id in self.bricks_by_id:
                            self.damage_brick(hit_id)

            elif powerup["type"] == POWERUP_ALIEN:
                if powerup["state"] == "flight":
                    self.canvas.move(body_id, 0, powerup["body_vy"])
                    self.canvas.move(aux_id, 0, powerup["body_vy"])
                    body_coords = self.canvas.coords(body_id)
                    if len(body_coords) != 4:
                        self.remove_special_powerup(powerup)
                        continue

                    hits = self.canvas.find_overlapping(*body_coords)
                    for hit_id in hits:
                        if hit_id in self.bricks_by_id:
                            powerup["state"] = "wait"
                            powerup["target_brick_id"] = hit_id
                            powerup["activated_ms"] = self.clock_ms + ALIEN_INFECT_DELAY_MS
                            powerup["latch_until_ms"] = self.clock_ms + ALIEN_INFECT_DELAY_MS + ALIEN_INFECT_LIFETIME_MS
                            self.canvas.itemconfigure(aux_id, state="normal")
                            self.canvas.coords(aux_id, body_coords[0] - 6, body_coords[1] - 6, body_coords[2] + 6, body_coords[3] + 6)
                            break
                elif powerup["state"] == "wait":
                    body_coords = self.canvas.coords(body_id)
                    if len(body_coords) != 4:
                        self.remove_special_powerup(powerup)
                        continue

                    self.canvas.coords(aux_id, body_coords[0] - 6, body_coords[1] - 6, body_coords[2] + 6, body_coords[3] + 6)
                    if self.clock_ms >= powerup["activated_ms"]:
                        self.queue_alien_infection(powerup["target_brick_id"], self.clock_ms)
                        self.remove_special_powerup(powerup)


    def laser_active(self) -> bool:
        return self.clock_ms < self.laser_until_ms

    def can_fire_laser(self) -> bool:
        return self.state == "playing" and self.laser_active() and self.clock_ms - self.last_laser_fire_ms >= LASER_FIRE_INTERVAL_MS

    def activate_laser(self) -> None:
        self.laser_until_ms = max(self.laser_until_ms, self.clock_ms) + LASER_POWER_DURATION_MS

    def fire_laser(self) -> None:
        paddle_left, paddle_top, paddle_right, _paddle_bottom = self.canvas.coords(self.paddle_id)
        paddle_center = (paddle_left + paddle_right) / 2
        left = paddle_center - LASER_WIDTH / 2
        right = paddle_center + LASER_WIDTH / 2
        top = paddle_top - LASER_HEIGHT
        bottom = paddle_top
        laser_id = self.canvas.create_rectangle(left, top, right, bottom, fill=LASER_COLOR, outline=LASER_COLOR, tags=("laser",))
        self.lasers.append(laser_id)
        self.last_laser_fire_ms = self.clock_ms

    def spawn_powerup(self, x: float, y: float, powerup_type: str | None = None) -> None:
        half_size = POWERUP_SIZE / 2
        if powerup_type not in POWERUP_LABELS:
            powerup_type = random.choice(POWERUP_DROP_TYPES)
        label_text, label_color = POWERUP_LABELS[powerup_type]
        item_id = self.canvas.create_oval(
            x - half_size,
            y - half_size,
            x + half_size,
            y + half_size,
            fill=label_color,
            outline=label_color,
            tags=("powerup",),
        )
        label_id = self.canvas.create_text(
            x,
            y - POWERUP_TEXT_OFFSET,
            text=label_text,
            fill=label_color,
            font=("Segoe UI", 8, "bold"),
            tags=("powerup",),
        )
        self.powerups.append({"shape": item_id, "label": label_id, "type": powerup_type})

    def damage_brick(self, item_id: int, amount: int = 1, drop_powerup: bool = True, force_drop_powerup: bool = False, forced_powerup_type: str | None = None) -> bool:
        brick = self.bricks_by_id.get(item_id)
        if brick is None:
            return False

        brick["health"] -= amount
        self.score += 10 * amount

        if brick["health"] <= 0:
            coords = self.canvas.coords(item_id)
            if drop_powerup and len(coords) == 4 and (force_drop_powerup or random.random() < POWERUP_DROP_CHANCE):
                x1, y1, x2, y2 = coords
                self.spawn_powerup((x1 + x2) / 2, (y1 + y2) / 2, forced_powerup_type)

            self.canvas.delete(item_id)
            self.bricks_by_id.pop(item_id, None)
            self.bricks_remaining -= 1

            if self.bricks_remaining <= 0:
                self.state = "win"
        else:
            if brick["electrified"]:
                fill_color = ELECTRIFIED_COLOR
            else:
                fill_color = BRICK_HEALTH_COLORS[brick["health"]]
            self.canvas.itemconfig(item_id, fill=fill_color, outline=BG_COLOR)

        return True

    def destroy_brick(self, item_id: int, drop_powerup: bool = True, force_drop_powerup: bool = False, forced_powerup_type: str | None = None) -> bool:
        brick = self.bricks_by_id.get(item_id)
        if brick is None:
            return False

        return self.damage_brick(item_id, amount=brick["health"], drop_powerup=drop_powerup, force_drop_powerup=force_drop_powerup, forced_powerup_type=forced_powerup_type)

    def electrify_brick(self, item_id: int) -> bool:
        brick = self.bricks_by_id.get(item_id)
        if brick is None or brick["electrified"]:
            return False

        brick["electrified"] = True
        brick["electrified_until_ms"] = self.clock_ms + BRICK_ELECTRIC_DURATION_MS
        self.canvas.itemconfig(item_id, fill=ELECTRIFIED_COLOR, outline=ELECTRIFIED_COLOR)
        return True

    def electrify_brick_cluster(self, item_id: int) -> None:
        coords = self.canvas.coords(item_id)
        if len(coords) != 4:
            return

        x1, y1, x2, y2 = coords
        hits = self.canvas.find_overlapping(
            x1 - BRICK_WIDTH / 2,
            y1 - BRICK_HEIGHT,
            x2 + BRICK_WIDTH / 2,
            y2 + BRICK_HEIGHT,
        )

        for hit_id in hits:
            if hit_id in self.bricks_by_id:
                self.electrify_brick(hit_id)

    def handle_space(self, _event: tk.Event | None = None) -> None:
        if self.screen != "game":
            return

        if any(ball["attached"] for ball in self.balls) or any(powerup["state"] == "held" for powerup in self.special_powerups):
            self.launch_ball()
            return

        if self.state == "ready":
            self.launch_ball()
        elif self.state == "playing" and self.can_fire_laser():
            self.fire_laser()
        elif self.state in {"game_over", "win"}:
            self.reset_game()
            self.launch_ball()

    def move_paddle(self) -> None:
        delta = 0.0
        if self.left_pressed and not self.right_pressed:
            delta = -PADDLE_SPEED * self.speed_multiplier
        elif self.right_pressed and not self.left_pressed:
            delta = PADDLE_SPEED * self.speed_multiplier

        if delta:
            playfield_width = self.gameplay_width()
            self.paddle_x = clamp(self.paddle_x + delta, PADDLE_WIDTH / 2, playfield_width - PADDLE_WIDTH / 2)

        self.place_paddle()

    def handle_wall_collisions(self, ball: BallSpec) -> None:
        ball_id = int(ball["id"])
        ball_left, ball_top, ball_right, ball_bottom = self.canvas.bbox(ball_id)
        playfield_width = self.gameplay_width()

        if ball_left <= 0:
            self.canvas.move(ball_id, -ball_left, 0)
            ball["dx"] = abs(float(ball["dx"]))
        elif ball_right >= playfield_width:
            self.canvas.move(ball_id, playfield_width - ball_right, 0)
            ball["dx"] = -abs(float(ball["dx"]))

        if ball_top <= 0:
            self.canvas.move(ball_id, 0, -ball_top)
            ball["dy"] = abs(float(ball["dy"]))

    def handle_paddle_collision(self, ball: BallSpec) -> None:
        ball_id = int(ball["id"])
        ball_left, ball_top, ball_right, ball_bottom = self.canvas.bbox(ball_id)
        paddle_coords = self.canvas.coords(self.paddle_id)
        if len(paddle_coords) != 4:
            return

        paddle_left, paddle_top, paddle_right, paddle_bottom = paddle_coords
        ball_dy = float(ball["dy"])

        if ball_bottom < paddle_top or ball_dy <= 0:
            return

        overlap_x = min(ball_right, paddle_right) - max(ball_left, paddle_left)
        overlap_y = min(ball_bottom, paddle_bottom) - max(ball_top, paddle_top)

        if overlap_x <= 0 or overlap_y <= 0:
            return

        paddle_center = (paddle_left + paddle_right) / 2
        ball_center = (ball_left + ball_right) / 2
        offset = clamp((ball_center - paddle_center) / (PADDLE_WIDTH / 2), -1.0, 1.0)

        ball["dx"] = offset * MAX_BOUNCE_X
        vertical_speed = math.sqrt(max(BALL_SPEED * BALL_SPEED - float(ball["dx"]) * float(ball["dx"]), MIN_BOUNCE_Y * MIN_BOUNCE_Y))
        ball["dy"] = -vertical_speed
        self.canvas.move(ball_id, 0, paddle_top - ball_bottom - 1)

    def handle_brick_collision(self, ball: BallSpec) -> None:
        ball_id = int(ball["id"])
        ball_left, ball_top, ball_right, ball_bottom = self.canvas.bbox(ball_id)
        hits = [item_id for item_id in self.canvas.find_overlapping(ball_left, ball_top, ball_right, ball_bottom) if item_id in self.bricks_by_id]

        if not hits:
            return

        if ball["enhancement"] == BALL_EFFECT_RADIOACTIVE:
            for item_id in hits:
                self.destroy_brick(item_id, drop_powerup=False)
            return

        hit_id = hits[0]
        brick_left, brick_top, brick_right, brick_bottom = self.canvas.coords(hit_id)
        overlap_x = min(ball_right, brick_right) - max(ball_left, brick_left)
        overlap_y = min(ball_bottom, brick_bottom) - max(ball_top, brick_top)
        if overlap_x <= 0 or overlap_y <= 0:
            return

        ball_center_x = (ball_left + ball_right) / 2
        ball_center_y = (ball_top + ball_bottom) / 2
        brick_center_x = (brick_left + brick_right) / 2
        brick_center_y = (brick_top + brick_bottom) / 2

        if overlap_x < overlap_y:
            shift = overlap_x + 1
            self.canvas.move(ball_id, -shift if ball_center_x < brick_center_x else shift, 0)
            ball["dx"] = -float(ball["dx"])
        else:
            shift = overlap_y + 1
            self.canvas.move(ball_id, 0, -shift if ball_center_y < brick_center_y else shift)
            ball["dy"] = -float(ball["dy"])

        if ball["enhancement"] == BALL_EFFECT_ELECTRIC:
            self.electrify_brick_cluster(hit_id)
        else:
            self.damage_brick(hit_id)

    def update_powerups(self) -> None:
        paddle_coords = self.canvas.coords(self.paddle_id)
        if len(paddle_coords) != 4:
            return

        paddle_left, paddle_top, paddle_right, paddle_bottom = paddle_coords

        for powerup in self.powerups[:]:
            shape_id = int(powerup["shape"])
            label_id = int(powerup["label"])
            self.canvas.move(shape_id, 0, POWERUP_SPEED)
            self.canvas.move(label_id, 0, POWERUP_SPEED)
            coords = self.canvas.bbox(shape_id)
            if not coords:
                self.powerups.remove(powerup)
                continue

            left, top, right, bottom = coords
            if top >= HEIGHT:
                self.canvas.delete(shape_id)
                self.canvas.delete(label_id)
                self.powerups.remove(powerup)
                continue

            overlap_x = min(right, paddle_right) - max(left, paddle_left)
            overlap_y = min(bottom, paddle_bottom) - max(top, paddle_top)
            if overlap_x > 0 and overlap_y > 0:
                self.canvas.delete(shape_id)
                self.canvas.delete(label_id)
                self.powerups.remove(powerup)
                self.apply_powerup_effect(powerup["type"])

    def update_lasers(self) -> None:
        for item_id in self.lasers[:]:
            self.canvas.move(item_id, 0, -LASER_SPEED)
            coords = self.canvas.bbox(item_id)
            if not coords:
                self.lasers.remove(item_id)
                continue

            left, top, right, bottom = coords
            if bottom <= 0:
                self.canvas.delete(item_id)
                self.lasers.remove(item_id)
                continue

            hits = self.canvas.find_overlapping(left, top, right, bottom)
            destroyed = False
            for hit_id in hits:
                if self.destroy_brick(hit_id):
                    destroyed = True
                    break

            if destroyed:
                self.canvas.delete(item_id)
                self.lasers.remove(item_id)

    def update_electrified_bricks(self) -> None:
        for item_id, brick in list(self.bricks_by_id.items()):
            if not brick["electrified"]:
                continue

            if self.clock_ms >= brick["electrified_until_ms"]:
                self.destroy_brick(item_id, drop_powerup=True)

    def probe_bbox(self, probe_id: int) -> tuple[float, float, float, float]:
        coords = self.canvas.bbox(probe_id)
        if len(coords) != 4:
            return (0.0, 0.0, 0.0, 0.0)

        return coords[0], coords[1], coords[2], coords[3]

    def probe_damage_bricks(self, probe_id: int) -> None:
        left, top, right, bottom = self.probe_bbox(probe_id)
        if right <= left or bottom <= top:
            return

        hits = self.canvas.find_overlapping(left, top, right, bottom)
        for hit_id in hits:
            if hit_id in self.bricks_by_id:
                self.damage_brick(hit_id)

    def update_probes(self) -> None:
        for probe in self.probes[:]:
            probe_id = int(probe["id"])
            probe_left, probe_top, probe_right, probe_bottom = self.probe_bbox(probe_id)
            if probe_right <= probe_left or probe_bottom <= probe_top:
                self.probes.remove(probe)
                continue

            probe_center_x = (probe_left + probe_right) / 2
            probe_center_y = (probe_top + probe_bottom) / 2

            if probe["state"] == "fly":
                target_ball_id = probe["target_ball_id"]
                target_ball = self.get_ball_by_id(target_ball_id) if target_ball_id != -1 else None
                if target_ball is None:
                    target_ball_id = self.nearest_ball_id(probe_center_x, probe_center_y)
                    probe["target_ball_id"] = target_ball_id
                    target_ball = self.get_ball_by_id(target_ball_id) if target_ball_id != -1 else None

                if target_ball is None:
                    self.probe_damage_bricks(probe_id)
                    continue

                target_left, target_top, target_right, target_bottom = self.ball_coords(target_ball)
                target_center_x = (target_left + target_right) / 2
                target_center_y = (target_top + target_bottom) / 2
                delta_x = target_center_x - probe_center_x
                delta_y = target_center_y - probe_center_y
                distance = math.hypot(delta_x, delta_y)
                if distance <= PROBE_ORBIT_LOCK_DISTANCE:
                    probe["state"] = "orbit"
                    probe["angle"] = math.atan2(delta_y, delta_x)
                    probe["orbit_radius"] = PROBE_ORBIT_RADIUS
                elif distance > 0:
                    step = min(PROBE_SPEED, distance)
                    self.canvas.move(probe_id, delta_x / distance * step, delta_y / distance * step)

            elif probe["state"] == "orbit":
                target_ball = self.get_ball_by_id(probe["target_ball_id"])
                if target_ball is None:
                    probe["state"] = "fly"
                    probe["target_ball_id"] = -1
                    self.probe_damage_bricks(probe_id)
                    continue

                target_left, target_top, target_right, target_bottom = self.ball_coords(target_ball)
                target_center_x = (target_left + target_right) / 2
                target_center_y = (target_top + target_bottom) / 2
                probe["angle"] += PROBE_ORBIT_STEP
                new_center_x = target_center_x + probe["orbit_radius"] * math.cos(probe["angle"])
                new_center_y = target_center_y + probe["orbit_radius"] * math.sin(probe["angle"])
                self.canvas.coords(
                    probe_id,
                    new_center_x - PROBE_RADIUS,
                    new_center_y - PROBE_RADIUS,
                    new_center_x + PROBE_RADIUS,
                    new_center_y + PROBE_RADIUS,
                )

            self.probe_damage_bricks(probe_id)

    def handle_bottom_loss(self) -> None:
        lost_any = False
        for ball in self.active_balls():
            _, _, _, ball_bottom = self.ball_coords(ball)
            if ball_bottom < HEIGHT:
                continue

            ball_id = int(ball["id"])
            self.canvas.delete(ball_id)
            self.balls.remove(ball)
            lost_any = True

        if not lost_any:
            return

        if self.active_balls():
            return

        self.lives -= 1
        if self.lives <= 0:
            self.state = "game_over"
        else:
            self.state = "ready"
            if not any(ball["attached"] for ball in self.balls):
                self.add_attached_ball()
            self.position_attached_balls()

    def refresh_hud(self) -> None:
        laser_status = ""
        if self.laser_active():
            remaining = max(0.0, (self.laser_until_ms - self.clock_ms) / 1000)
            laser_status = f"    Laser: {remaining:0.1f}s"

        self.canvas.itemconfig(
            self.status_id,
            text=f"Score: {self.score}    Lives: {self.lives}    Bricks: {self.bricks_remaining}    Balls: {len(self.balls)}    Speed: x{self.speed_multiplier:g}{laser_status}",
        )

    def refresh_message(self) -> None:
        if self.state == "ready":
            self.canvas.itemconfig(self.help_id, text="Press Space to launch", state="normal")
            self.canvas.itemconfig(
                self.subtext_id,
                text="Left/Right to move, Space to launch",
                state="normal",
            )
        elif self.state == "game_over":
            self.canvas.itemconfig(self.help_id, text="Game Over", state="normal")
            self.canvas.itemconfig(self.subtext_id, text="Press Space to restart", state="normal")
        elif self.state == "win":
            self.canvas.itemconfig(self.help_id, text="You Win", state="normal")
            self.canvas.itemconfig(self.subtext_id, text="Press Space to play again", state="normal")
        else:
            self.canvas.itemconfig(self.help_id, state="hidden")
            self.canvas.itemconfig(self.subtext_id, state="hidden")

    def tick(self) -> None:
        self.clock_ms += FPS_DELAY_MS
        if self.screen == "game":
            self.move_paddle()

            if self.state == "ready":
                self.sync_attached_ball_to_paddle()

            if self.state not in {"game_over", "win"}:
                for ball in self.active_balls():
                    ball_id = int(ball["id"])
                    self.canvas.move(ball_id, float(ball["dx"]) * self.speed_multiplier, float(ball["dy"]) * self.speed_multiplier)
                    self.handle_wall_collisions(ball)
                    self.handle_paddle_collision(ball)
                    self.handle_brick_collision(ball)

                self.handle_bottom_loss()

            if self.state not in {"game_over", "win"}:
                self.update_powerups()
                self.update_lasers()
                self.update_ball_enhancements()
                self.update_special_powerups()
                self.update_electrified_bricks()
                self.update_alien_infections()
                self.update_probes()

            self.refresh_hud()
            self.refresh_message()

            if self.mode == "debug":
                self.draw_debug_panel()

        self.root.after(FPS_DELAY_MS, self.tick)


def main() -> None:
    root = tk.Tk()
    BreakoutGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()