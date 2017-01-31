import pygame as pg
from os import path
from collections import deque
from random import choice, uniform
vec = pg.math.Vector2

TILESIZE = 48
GRIDWIDTH = 30
GRIDHEIGHT = 15
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
FPS = 60
MOB_SPEED = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (140, 140, 140)

font_name = pg.font.match_font('hack')
def draw_text(text, size, color, x, y, align="topleft"):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    screen.blit(text_surface, text_rect)

class Mob(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        spawn = vec(choice(list(paths.keys())))
        # pixel position
        self.pos = vec(spawn.x * TILESIZE + TILESIZE / 2, spawn.y * TILESIZE + TILESIZE / 2)
        self.rect.center = self.pos

    @property
    def grid_pos(self):
        # find grid pos
        return (int(self.pos.x // TILESIZE), int(self.pos.y // TILESIZE))

    def update(self):
        if self.grid_pos == start:
            self.kill()
            return
        # destination is center of next square
        tx, ty = paths[self.grid_pos]
        self.target = vec(tx * TILESIZE + TILESIZE / 2, ty * TILESIZE + TILESIZE / 2)
        vel = (self.target - self.pos).normalize() * MOB_SPEED
        self.pos += vel  # .rotate(uniform(-35, 35))
        self.rect.center = self.pos

class Queue:
    # convenience wrapper around collections.deque
    def __init__(self):
        self.elements = deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        # comment/uncomment this for diagonals:
        self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    def in_bounds(self, loc):
        x, y = loc
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, loc):
        return loc not in self.walls

    def neighbors(self, loc):
        x, y = loc
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        # aesthetics
        if (x + y) % 2:
            results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

def draw_grid(grid, paths, dist):
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))
    for wall in grid.walls:
        x, y = wall
        r = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, LIGHTGRAY, r)
    screen.blit(home_img, (start[0] * TILESIZE, start[1] * TILESIZE))

def breadth_first_search2(graph, start):
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None
    distance = {}
    distance[start] = 0

    while not frontier.empty():
        current = frontier.get()
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
                distance[next] = distance[current] + 1
    return came_from, distance

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# load map
game_folder = path.dirname(__file__)
data = []
with open(path.join(game_folder, 'mob_test_map.txt'), 'rt') as f:
    for line in f:
        data.append(line.strip())

# icons
icon_folder = path.join(path.join(game_folder, '..'), 'icons')
home_img = pg.image.load(path.join(icon_folder, 'target.png')).convert_alpha()
home_img = pg.transform.scale(home_img, (int(TILESIZE), int(TILESIZE)))
home_img.fill((255, 0, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
arrows = {}
for d in ['Up', 'Down', 'Right', 'Left']:
    fname = 'arrow%s.png' % d
    img = pg.image.load(path.join(icon_folder, fname)).convert_alpha()
    arrows[d] = pg.transform.scale(img, (int(TILESIZE / 1.2), int(TILESIZE / 1.2)))

all_sprites = pg.sprite.Group()
g = SquareGrid(30, 15)
# add walls
for row, tiles in enumerate(data):
    for col, tile in enumerate(tiles):
        if tile == '1':
            g.walls.append((col, row))

start = (8, 9)
paths, dist = breadth_first_search2(g, start)

pg.time.set_timer(pg.USEREVENT, 50)
paused = False
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
        if event.type == pg.USEREVENT and not paused:
            Mob()
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = pg.mouse.get_pos()
            x = mpos[0] // TILESIZE
            y = mpos[1] // TILESIZE
            if event.button == 1:
                # spawn/del walls
                if (x, y) in g.walls:
                    g.walls.remove((x, y))
                else:
                    all_sprites.empty()
                    g.walls.append((x, y))
            elif event.button == 3:
                # move destination
                if (x, y) not in g.walls:
                    start = (x, y)
            paths, dist = breadth_first_search2(g, start)

    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    draw_grid(g, paths, dist)
    all_sprites.draw(screen)
    pg.display.flip()
    update = False
