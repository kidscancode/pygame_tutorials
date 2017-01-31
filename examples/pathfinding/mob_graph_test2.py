import pygame as pg
from os import path
import heapq
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
FOREST = (34, 57, 10)
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
        # destination is center of next square - just continue if on wall tile
        if self.grid_pos in paths:
            self.target_tile = self.grid_pos + paths[self.grid_pos]
            dest = (self.target_tile.x * TILESIZE + TILESIZE / 2, self.target_tile.y * TILESIZE + TILESIZE / 2)
            self.vel = (dest - self.pos).normalize() * MOB_SPEED
        self.pos += self.vel  # .rotate(uniform(-35, 35))
        self.rect.center = self.pos

class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        # comment/uncomment this for diagonals:
        # self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)

class WeightedGrid(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 1) + 10
        else:
            return self.weights.get(to_node, 1) + 14

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)
        for tile in self.weights:
            x, y = tile
            rect = pg.Rect(x * TILESIZE + 3, y * TILESIZE + 3, TILESIZE - 3, TILESIZE - 3)
            pg.draw.rect(screen, FOREST, rect)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))
    screen.blit(home_img, (start[0] * TILESIZE, start[1] * TILESIZE))

def vec2int(v):
    return (int(v.x), int(v.y))

def dijkstra_search(graph, start):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            next_cost = cost[current] + graph.cost(current, next)
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                priority = next_cost
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    return path

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# icons
icon_dir = path.join(path.dirname(__file__), '../icons')
home_img = pg.image.load(path.join(icon_dir, 'home.png')).convert_alpha()
home_img = pg.transform.scale(home_img, (50, 50))
home_img.fill((0, 255, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
arrows = {}
arrow_img = pg.image.load(path.join(icon_dir, 'arrowRight.png')).convert_alpha()
arrow_img = pg.transform.scale(arrow_img, (50, 50))
for dir in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
    arrows[dir] = pg.transform.rotate(arrow_img, vec(dir).angle_to(vec(1, 0)))

all_sprites = pg.sprite.Group()
g = WeightedGrid(30, 15)
walls = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (6, 7), (5, 7), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8), (12, 9), (12, 10), (12, 11), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10), (19, 10), (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6), (14, 0), (14, 1), (9, 2), (9, 1), (7, 3), (8, 3), (10, 3), (9, 3), (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11), (1, 11), (2, 11), (21, 2), (20, 11), (20, 12), (23, 13), (23, 14), (24, 10), (25, 10), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (5, 3), (6, 3), (5, 4)]
# walls = []
for wall in walls:
    g.walls.append(vec(wall))
terrain = [(11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (16, 8), (15, 8), (14, 8), (13, 8), (12, 8), (11, 8), (10, 8), (11, 9), (12, 9), (13, 9), (14, 9), (15, 9), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (12, 11), (13, 11), (14, 11), (12, 5), (13, 5), (14, 5), (11, 5), (15, 5), (12, 4), (13, 4), (14, 4)]
terrain = []
for tile in terrain:
    g.weights[tile] = 15

start = vec(8, 9)
paths = dijkstra_search(g, start)

pg.time.set_timer(pg.USEREVENT, 20)
paused = True
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
            if event.key == pg.K_m:
                Mob()
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
                    g.walls.append(vec(x, y))
            elif event.button == 3:
                # move destination
                if (x, y) not in g.walls:
                    start = vec(x, y)
            paths = dijkstra_search(g, start)

    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    draw_grid()
    g.draw()
    # for loc in paths:
    #     x, y = loc
    #     v = paths[(x, y)]
    #     if v:
    #         img = arrows[vec2int(v)]
    #         x = x * TILESIZE + TILESIZE / 2
    #         y = y * TILESIZE + TILESIZE / 2
    #         r = img.get_rect(center=(x, y))
    #         screen.blit(img, r)
    all_sprites.draw(screen)
    pg.display.flip()
    update = False
