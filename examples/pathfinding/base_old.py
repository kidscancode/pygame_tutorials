# Pathfinding example
# KidsCanCode 2016
import pygame as pg
from os import path
from random import randint, uniform
vec = pg.math.Vector2

TILESIZE = 48
GRIDWIDTH = 32
GRIDHEIGHT = 20
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
MOB_SIZE = 10
MAX_SPEED = 4
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (140, 140, 140)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

def draw_dest():
    center = (int(destination.x * TILESIZE + TILESIZE / 2), int(destination.y * TILESIZE + TILESIZE / 2))
    dest_rect.center = center
    screen.blit(dest_img, dest_rect)

def draw_source():
    center = (int(source.x * TILESIZE + TILESIZE / 2), int(source.y * TILESIZE + TILESIZE / 2))
    source_rect.center = center
    screen.blit(source_img, source_rect)

def draw_walls():
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val:
                r = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                pg.draw.rect(screen, LIGHTGRAY, r)


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
# load map
game_folder = path.dirname(__file__)
grid = []
with open(path.join(game_folder, 'map.txt'), 'rt') as f:
    for line in f:
        row = []
        line = line.strip()
        for char in line:
            row.append(int(char))
        grid.append(row)

# icons
icon_folder = path.join(path.join(game_folder, '..'), 'icons')
dest_img = pg.image.load(path.join(icon_folder, 'target.png')).convert_alpha()
dest_img = pg.transform.scale(dest_img, (int(TILESIZE * 1.2), int(TILESIZE * 1.2)))
dest_rect = dest_img.get_rect()
dest_img.fill((255, 0, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
source_img = pg.image.load(path.join(icon_folder, 'home.png')).convert_alpha()
source_img = pg.transform.scale(source_img, (int(TILESIZE * 1.2), int(TILESIZE * 1.2)))
source_rect = source_img.get_rect()
source_img.fill((0, 255, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
destination = vec(12, 2)
source = vec(12, 15)

paused = False
show_debug = False
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                paused = not paused
            if event.key == pg.K_d:
                show_debug = not show_debug
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = pg.mouse.get_pos()
            x = mpos[0] // TILESIZE
            y = mpos[1] // TILESIZE
            if event.button == 1:
                # spawn/del walls
                if grid[y][x] == 1:
                    grid[y][x] = 0
                else:
                    grid[y][x] = 1
            elif event.button == 3:
                # move destination
                if not grid[y][x]:
                    destination = vec(x, y)

    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    if show_debug:
        pass
    draw_grid()
    draw_walls()
    draw_dest()
    draw_source()
    all_sprites.draw(screen)
    pg.display.flip()
