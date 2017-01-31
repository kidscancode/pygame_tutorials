import pygame as pg
import heapq
from os import path
from random import choice
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
        self.on_path = False

    @property
    def grid_pos(self):
        # find grid pos
        return (int(self.pos.x // TILESIZE), int(self.pos.y // TILESIZE))

    def update(self):
        if self.grid_pos == goal:
            self.kill()
            return
        # if in a node tile, steer to next node

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

class WeightedMesh:
    # edges = {(1, 1): {(4, 11): 10, (9, 7): 25}}
    def __init__(self):
        # locations of nodes on map
        # connections and costs from node to node
        self.edges = {}
        self.edges = {(0, 8): {(2, 8): 20, (0, 1): 70, (0, 13): 50},
                      (0, 1): {(0, 8): 70, (4, 0): 44},
                      (2, 8): {(0, 8): 20},
                      (4, 0): {(0, 1): 44, (8, 2): 48},
                      (8, 2): {(4, 0): 48, (11, 1): 34, (11, 6): 52},
                      (0, 13): {(0, 8): 50, (6, 13): 60},
                      (6, 13): {(0, 13): 60, (11, 10): 72},
                      (11, 10): {(6, 13): 72, (13, 10): 20},
                      (13, 10): {(11, 10): 20, (15, 7): 38, (17, 13): 52},
                      (11, 1): {(8, 2): 34, (15, 3): 48},
                      (11, 6): {(8, 2): 52, (15, 7): 44},
                      (15, 7): {(15, 3): 40, (11, 6): 44, (13, 10): 38, (20, 7): 50},
                      (15, 3): {(11, 1): 48, (15, 7): 40, (17, 2): 24},
                      (17, 2): {(15, 3): 24, (20, 2): 30},
                      (20, 2): {(17, 2): 30, (20, 7): 50, (23, 1): 34},
                      (23, 1): {(20, 2): 34, (27, 1): 40},
                      (27, 1): {(23, 1): 40, (26, 4): 34},
                      (26, 4): {(27, 1): 34, (25, 7): 34},
                      (25, 7): {(26, 4): 34, (20, 7): 50, (25, 10): 30},
                      (20, 7): {(15, 7): 50, (20, 2): 50, (25, 7): 50},
                      (25, 10): {(25, 7): 30, (22, 12): 38},
                      (22, 12): {(25, 10): 38, (17, 13): 54},
                      (17, 13): {(13, 10): 52, (22, 12): 54}}

    def find_neighbors(self, node):
        return list(self.edges[node].keys())

    def find_nearest(self, tile):
        return min(self.edges.keys(), key=lambda n: (abs(n[0] - tile[0]) + abs(n[1] - tile[1])))

    def cost(self, from_node, to_node):
        return self.edges[from_node][to_node]

    def draw(self):
        for node in self.edges.keys():
            x = int(node[0] * TILESIZE + TILESIZE / 2)
            y = int(node[1] * TILESIZE + TILESIZE / 2)
            pg.draw.circle(screen, CYAN, (x, y), 10)
            for c in self.edges[node]:
                cx = c[0] * TILESIZE + TILESIZE / 2
                cy = c[1] * TILESIZE + TILESIZE / 2
                pg.draw.line(screen, CYAN, (x, y), (cx, cy), 10)

class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

def draw_icons():
    goal_center = (goal[0] * TILESIZE + TILESIZE / 2, goal[1] * TILESIZE + TILESIZE / 2)
    screen.blit(home_img, home_img.get_rect(center=goal_center))
    start_center = (start[0] * TILESIZE + TILESIZE / 2, start[1] * TILESIZE + TILESIZE / 2)
    screen.blit(cross_img, cross_img.get_rect(center=start_center))

def vec2int(v):
    return (int(v.x), int(v.y))

def t2px(tile):
    x, y = tile
    x = x * TILESIZE + TILESIZE / 2
    y = y * TILESIZE + TILESIZE / 2
    return (x, y)

def dijkstra_search(graph, start):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    path = {}
    cost = {}
    path[start] = None
    cost[start] = 0

    while not frontier.empty():
        current = frontier.get()
        for next in graph.find_neighbors(current):
            next_cost = cost[current] + graph.cost(current, next)
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                priority = next_cost
                frontier.put(next, priority)
                path[next] = current
    return path

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# icons
icon_dir = path.join(path.dirname(__file__), '../icons')
home_img = pg.image.load(path.join(icon_dir, 'home.png')).convert_alpha()
home_img = pg.transform.scale(home_img, (50, 50))
home_img.fill((0, 255, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
cross_img = pg.image.load(path.join(icon_dir, 'cross.png')).convert_alpha()
cross_img = pg.transform.scale(cross_img, (50, 50))
cross_img.fill((255, 0, 0, 255), special_flags=pg.BLEND_RGBA_MULT)

all_sprites = pg.sprite.Group()
g = SquareGrid(30, 15)
m = WeightedMesh()
# add walls
walls = [(3, 2), (2, 2), (4, 1), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (6, 5), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (9, 9), (9, 8), (9, 6), (9, 5), (7, 5), (8, 5), (6, 11), (6, 12), (6, 14), (10, 7), (9, 7), (11, 7), (12, 7), (12, 9), (12, 8), (12, 11), (12, 12), (12, 13), (12, 14), (11, 0), (11, 2), (11, 3), (11, 4), (12, 4), (13, 4), (13, 5), (14, 5), (16, 5), (17, 5), (18, 5), (19, 5), (17, 4), (17, 3), (17, 0), (17, 1), (21, 5), (22, 5), (23, 5), (23, 4), (23, 3), (23, 2), (23, 0), (24, 4), (25, 4), (27, 4), (17, 6), (17, 8), (17, 9), (17, 10), (17, 11), (17, 12), (17, 14), (18, 9), (20, 9), (19, 9), (21, 9), (22, 9), (23, 9), (24, 9), (26, 9), (27, 9), (22, 10), (22, 11), (22, 13), (22, 14), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 9), (1, 10)]
for wall in walls:
    g.walls.append(vec(wall))

goal = (0, 1)
start = (17, 13)
paths = dijkstra_search(m, m.find_nearest(goal))
print(paths)


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
        # if event.type == pg.USEREVENT and not paused:
        #     Mob()
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = pg.mouse.get_pos()
            x = mpos[0] // TILESIZE
            y = mpos[1] // TILESIZE
            if event.button == 1:
                # move start
                start = m.find_nearest((x, y))
            if event.button == 3:
                # move goal
                goal = m.find_nearest((x, y))
            paths = dijkstra_search(m, m.find_nearest(goal))

    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    draw_grid()
    g.draw()
    m.draw()
    # draw path from start to goal
    current = start
    l = 0
    while current != goal:
        next_node = paths[current]
        current_tile = t2px(current)
        next_tile = t2px(next_node)
        pg.draw.line(screen, RED, current_tile, next_tile, 8)
        # l += m.cost(current, next_node)
        current = paths[current]
    # for n in disp_nodes:
    #     screen_x = n[0] * TILESIZE + TILESIZE / 2
    #     screen_y = n[1] * TILESIZE + TILESIZE / 2
    # draw_text(str(l), 12, WHITE, 10, 10, align="topleft")
    draw_icons()
    pg.display.flip()
