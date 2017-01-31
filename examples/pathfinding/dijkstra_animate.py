import pygame as pg
from os import path
from collections import deque
import heapq
vec = pg.math.Vector2

TILESIZE = 48
GRIDWIDTH = 28
GRIDHEIGHT = 15
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FOREST = (34, 57, 10)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (90, 90, 90)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        # comment/uncomment this for diagonals:
        self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

class WeightedGrid(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 10
        else:
            return self.weights.get(to_node, 0) + 14

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)
        for tile in self.weights:
            x, y = tile
            rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pg.draw.rect(screen, FOREST, rect)

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def vec2int(v):
    return (int(v.x), int(v.y))

def draw_icons():
    start_center = (start.x * TILESIZE + TILESIZE / 2, start.y * TILESIZE + TILESIZE / 2)
    screen.blit(home_img, home_img.get_rect(center=start_center))
    goal_center = (goal.x * TILESIZE + TILESIZE / 2, goal.y * TILESIZE + TILESIZE / 2)
    screen.blit(cross_img, cross_img.get_rect(center=goal_center))

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

icon_dir = path.join(path.dirname(__file__), '../icons')
home_img = pg.image.load(path.join(icon_dir, 'home.png')).convert_alpha()
home_img = pg.transform.scale(home_img, (50, 50))
home_img.fill((0, 255, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
cross_img = pg.image.load(path.join(icon_dir, 'cross.png')).convert_alpha()
cross_img = pg.transform.scale(cross_img, (50, 50))
cross_img.fill((255, 0, 0, 255), special_flags=pg.BLEND_RGBA_MULT)

sg = WeightedGrid(GRIDWIDTH, GRIDHEIGHT)
walls = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (6, 7), (5, 7), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8), (12, 9), (12, 10), (12, 11), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10), (19, 10), (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6), (14, 0), (14, 1), (9, 2), (9, 1), (7, 3), (8, 3), (10, 3), (9, 3), (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11), (1, 11), (2, 11), (21, 2), (20, 11), (20, 12), (23, 13), (23, 14), (24, 10), (25, 10), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (5, 3), (6, 3), (5, 4)]
# walls = []
for wall in walls:
    sg.walls.append(vec(wall))

terrain = [(12, 4), (13, 4), (14, 4), (11, 5), (12, 5), (13, 5), (14, 5), (15, 5), (15, 6), (14, 6), (12, 6), (11, 6), (10, 7), (10, 8), (11, 7), (11, 8), (12, 7), (12, 8), (13, 8), (14, 7), (14, 8), (15, 7), (15, 8), (16, 7), (16, 8), (15, 9), (14, 9), (13, 9), (12, 9), (11, 9), (11, 10), (12, 10), (12, 11), (13, 10), (13, 11), (14, 11), (14, 10), (15, 10), (9, 7), (8, 7), (8, 8), (9, 8), (10, 6), (9, 6), (8, 6), (10, 5), (9, 5), (8, 5), (11, 4), (10, 4), (9, 4), (8, 4), (7, 8), (6, 8)]
for tile in terrain:
    sg.weights[tile] = 8

start = vec(11, 14)
goal = vec(20, 0)

frontier = PriorityQueue()
frontier.put(vec2int(start), 0)
path = {}
cost = {}
visited = []
visited.append(start)
path[vec2int(start)] = None
cost[vec2int(start)] = 0

paused = True
running = True
done = False
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

    if not frontier.empty() and not paused and not done:
        current = frontier.get()
        if current == goal:
            done = True
        for next in sg.find_neighbors(current):
            new_cost = cost[current] + sg.cost(current, vec2int(next))
            if vec2int(next) not in cost or new_cost < cost[vec2int(next)]:
                cost[vec2int(next)] = new_cost
                priority = new_cost
                visited.append(next)
                frontier.put(vec2int(next), priority)
                path[vec2int(next)] = vec(current) - vec(next)

        # paused = True
    if frontier.empty():
        done = True

    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    #draw_grid()
    sg.draw()
    # for loc in visited:
    #     x, y = loc
    #     r = pg.Rect(x * TILESIZE + 3, y * TILESIZE + 3, TILESIZE - 3, TILESIZE - 3)
    #     pg.draw.rect(screen, (71, 130, 109), r)
    if not frontier.empty():
        for n in frontier.elements:
            x, y = n[1]
            r = pg.Rect(x * TILESIZE + 3, y * TILESIZE + 3, TILESIZE - 3, TILESIZE - 3)
            pg.draw.rect(screen, RED, r)
    if done:
        current = goal
        while current != start:
            # fill in current
            r = pg.Rect(current.x * TILESIZE + 9, current.y * TILESIZE + 9, TILESIZE - 14, TILESIZE - 14)
            pg.draw.rect(screen, YELLOW, r)
            # find next
            current = current + path[vec2int(current)]
    draw_icons()
    pg.display.flip()
