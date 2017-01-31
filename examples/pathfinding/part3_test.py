# Pathfinding - Part 2
# Breadth First Search (BFS)
# KidsCanCode 2017
import pygame as pg
from os import path
from collections import deque
vec = pg.math.Vector2

TILESIZE = 48
GRIDWIDTH = 28
GRIDHEIGHT = 15
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
MEDGRAY = (90, 90, 90)
LIGHTGRAY = (140, 140, 140)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.connections = [vec(1, 0), vec(0, -1), vec(-1, 0), vec(0, 1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        if (node.x + node.y) % 2:
            neighbors.reverse()
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

def vec2int(v):
    return (int(v.x), int(v.y))

def breadth_first_with_exit(graph, start, end):
    frontier = deque()
    frontier.append(start)
    path = {}
    path[vec2int(start)] = None
    while len(frontier) > 0:
        current = frontier.popleft()
        if current == end:
            break
        for next in graph.find_neighbors(current):
            if vec2int(next) not in path:
                frontier.append(next)
                path[vec2int(next)] = current - next
    return path

def draw_icons():
    home_center = (home.x * TILESIZE + TILESIZE / 2, home.y * TILESIZE + TILESIZE / 2)
    screen.blit(home_img, home_img.get_rect(center=home_center))
    start_center = (start.x * TILESIZE + TILESIZE / 2, start.y * TILESIZE + TILESIZE / 2)
    screen.blit(cross_img, cross_img.get_rect(center=start_center))

icon_dir = path.join(path.dirname(__file__), '../icons')
home_img = pg.image.load(path.join(icon_dir, 'home.png')).convert_alpha()
home_img = pg.transform.scale(home_img, (50, 50))
home_img.fill((0, 255, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
cross_img = pg.image.load(path.join(icon_dir, 'cross.png')).convert_alpha()
cross_img = pg.transform.scale(cross_img, (50, 50))
cross_img.fill((255, 0, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
arrows = {}
arrow_img = pg.image.load(path.join(icon_dir, 'arrowRight.png')).convert_alpha()
arrow_img = pg.transform.scale(arrow_img, (50, 50))
for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
    arrows[dir] = pg.transform.rotate(arrow_img, vec(dir).angle_to(vec(1, 0)))

g = SquareGrid(GRIDWIDTH, GRIDHEIGHT)
walls = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (6, 7), (5, 7), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8), (12, 9), (12, 10), (12, 11), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10), (19, 10), (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6), (14, 0), (14, 1), (9, 2), (9, 1), (7, 3), (8, 3), (10, 3), (9, 3), (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11), (1, 11), (2, 11), (21, 2), (20, 11), (20, 12), (23, 13), (23, 14), (24, 10), (25, 10), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (5, 3), (6, 3), (5, 4)]
for wall in walls:
    g.walls.append(vec(wall))
home = vec(14, 8)
start = vec(20, 0)
path = breadth_first_with_exit(g, home, start)

running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_m:
                # dump the wall list for saving
                print([(int(loc.x), int(loc.y)) for loc in g.walls])
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = vec(pg.mouse.get_pos()) // TILESIZE
            if event.button == 1:
                if mpos in g.walls:
                    g.walls.remove(mpos)
                else:
                    g.walls.append(mpos)
            if event.button == 2:
                start = mpos
            if event.button == 3:
                home = mpos
            path = breadth_first_with_exit(g, home, start)

    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    g.draw()
    # fill explored area
    for node in path:
        x, y = node
        rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, MEDGRAY, rect)
    draw_grid()
    # draw path
    current = start + path[vec2int(start)]
    while current != home:
        # fill in current
        x = current.x * TILESIZE + TILESIZE / 2
        y = current.y * TILESIZE + TILESIZE / 2
        img = arrows[vec2int(path[(current.x, current.y)])]
        r = img.get_rect(center=(x, y))
        screen.blit(img, r)
        # find next
        current = current + path[vec2int(current)]
    draw_icons()
    pg.display.flip()
