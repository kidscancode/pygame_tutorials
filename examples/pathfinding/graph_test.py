import pygame as pg
from os import path
from collections import deque

TILESIZE = 48
GRIDWIDTH = 30
GRIDHEIGHT = 15
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
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

font_name = pg.font.match_font('hack')
def draw_text(text, size, color, x, y, align="topleft"):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    screen.blit(text_surface, text_rect)

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

class SimpleGraph:
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        return self.edges[id]

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, loc):
        x, y = loc
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, loc):
        return loc not in self.walls

    def neighbors(self, loc):
        x, y = loc
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if test_h:
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

    if paths and not show_dist:
        for loc in paths:
            x, y = loc
            if not paths[loc]:
                screen.blit(home_img, (x * TILESIZE, y * TILESIZE))
            else:
                x1, y1 = paths[loc]
                if x == x1:
                    if y > y1:
                        dir = 'Up'
                    else:
                        dir = 'Down'
                elif y == y1:
                    if x > x1:
                        dir = 'Left'
                    else:
                        dir = 'Right'
                screen.blit(arrows[dir], (x * TILESIZE, y * TILESIZE))
    else:
        for loc in dist:
            x, y = loc
            sx = x * TILESIZE + TILESIZE / 2
            sy = y * TILESIZE + TILESIZE / 2
            if loc == start:
                screen.blit(home_img, (x * TILESIZE, y * TILESIZE))
            else:
                draw_text(str(dist[loc]), 18, WHITE, sx, sy, align="center")

def breadth_first_search1(graph, start):
    frontier = Queue()
    frontier.put(start)
    visited = {}
    visited[start] = True

    while not frontier.empty():
        current = frontier.get()
        print("Visiting %r" % current)
        for next in graph.neighbors(current):
            if next not in visited:
                frontier.put(next)
                visited[next] = True

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

# example_graph = SimpleGraph()
# example_graph.edges = {
#     'A': ['B'],
#     'B': ['A', 'C', 'D'],
#     'C': ['A'],
#     'D': ['E', 'A'],
#     'E': ['B']}
# breadth_first_search1(example_graph, 'A')

game_folder = path.dirname(__file__)
# icons
icon_folder = path.join(path.join(game_folder, '..'), 'icons')
home_img = pg.image.load(path.join(icon_folder, 'home.png')).convert_alpha()
home_img = pg.transform.scale(home_img, (int(TILESIZE / 1.2), int(TILESIZE / 1.2)))
home_img.fill((0, 255, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
arrows = {}
for d in ['Up', 'Down', 'Right', 'Left']:
    fname = 'arrow%s.png' % d
    img = pg.image.load(path.join(icon_folder, fname)).convert_alpha()
    arrows[d] = pg.transform.scale(img, (int(TILESIZE / 1.2), int(TILESIZE / 1.2)))

g = SquareGrid(30, 15)
start = (8, 7)
test_h = True
show_dist = False
paths, dist = breadth_first_search2(g, start)

update = True
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_h:
                test_h = not test_h
                paths, dist = breadth_first_search2(g, start)
            if event.key == pg.K_SPACE:
                show_dist = not show_dist
                update = True
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = pg.mouse.get_pos()
            x = mpos[0] // TILESIZE
            y = mpos[1] // TILESIZE
            if event.button == 1:
                # spawn/del walls
                if (x, y) in g.walls:
                    g.walls.remove((x, y))
                else:
                    g.walls.append((x, y))
            elif event.button == 3:
                # move destination
                if (x, y) not in g.walls:
                    start = (x, y)
            paths, dist = breadth_first_search2(g, start)
            update = True

    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    if update:
        screen.fill(DARKGRAY)
        draw_grid(g, paths, dist)
        pg.display.flip()
        update = False
