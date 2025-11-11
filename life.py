import pygame
import sys
import time
import json


def load_config(path="config.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Ошибка чтения config.json, используются значения по умолчанию:", e)
        return {}


class Field:
    def __init__(self, path, H, W):
        self.H = H
        self.W = W
        self.grid = self.read_field(path)

    def read_field(self, path):
        field = []
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                field.append([1 if c == "O" else 0 for c in line])
        return field

    def count_neighbours(self, x, y):
        n = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                nx = (x + dx) % self.W
                ny = (y + dy) % self.H
                n += self.grid[ny][nx]
        return n

    def next_generation(self, survive, birth):
        new = [[0] * self.W for _ in range(self.H)]
        for y in range(self.H):
            for x in range(self.W):
                n = self.count_neighbours(x, y)
                if self.grid[y][x] == 1:
                    new[y][x] = 1 if n in survive else 0
                else:
                    new[y][x] = 1 if n in birth else 0
        return new


def draw_field(screen, field, H, W, CELL_SIZE, bg_color, cell_color, text_color, speed_ms):
    screen.fill(bg_color)
    for y in range(H):
        for x in range(W):
            if field[y][x]:
                pygame.draw.rect(
                    screen,
                    cell_color,
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1),
                )
    font = pygame.font.SysFont("monospace", 16)
    pygame.display.flip()


def init_game(cfg):
    window_width = cfg.get("window_width", 800)
    window_height = cfg.get("window_height", 600)
    CELL_SIZE = cfg.get("cell_size", 10)
    PANEL_WIDTH = cfg.get("panel_width", 200)

    H = window_height // CELL_SIZE
    W = window_width // CELL_SIZE
    field = Field(cfg.get("field_path", "field.txt"), H, W)

    pygame.init()
    screen = pygame.display.set_mode((W * CELL_SIZE + PANEL_WIDTH, H * CELL_SIZE))
    pygame.display.set_caption("Game of Life")
    clock = pygame.time.Clock()
    return screen, clock, field, H, W, CELL_SIZE, PANEL_WIDTH


cfg = load_config("config.json")
FPS = cfg.get("fps", 30)
speed_ms = cfg.get("initial_speed_ms", 100)
bg_color = tuple(cfg.get("background_color", [0, 0, 0]))
cell_color = tuple(cfg.get("cell_color", [255, 0, 255]))
text_color = tuple(cfg.get("text_color", [255, 255, 255]))
survive = cfg.get("survive", [2, 3])
birth = cfg.get("birth", [3])
panel_color = tuple(cfg.get("panel_color", [30, 30, 30]))
panel_border_color = tuple(cfg.get("panel_border_color", [120, 120, 120]))
patterns = cfg.get("patterns", {})
