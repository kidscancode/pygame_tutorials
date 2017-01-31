# Pathfinding - Part 2
# Breadth First Search (BFS)
# KidsCanCode 2017
import pygame as pg
from os import path
import heapq
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
FOREST = (34, 57, 10)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
MEDGRAY = (75, 75, 75)
LIGHTGRAY = (140, 140, 140)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

font_name = pg.font.match_font('hack')
def draw_text(text, size, color, x, y, align="topleft"):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    screen.blit(text_surface, text_rect)

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
        # don't use this for diagonals:
        # if (node.x + node.y) % 2:
        #     neighbors.reverse()
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
            return self.weights.get(to_node, 0) + 10
        else:
            return self.weights.get(to_node, 0) + 14

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)
        for tile in self.weights:
            x, y = tile
            rect = pg.Rect(x * TILESIZE + 3, y * TILESIZE + 3, TILESIZE - 3, TILESIZE - 3)
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

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

def draw_icons():
    start_center = (goal.x * TILESIZE + TILESIZE / 2, goal.y * TILESIZE + TILESIZE / 2)
    screen.blit(home_img, home_img.get_rect(center=start_center))
    goal_center = (start.x * TILESIZE + TILESIZE / 2, start.y * TILESIZE + TILESIZE / 2)
    screen.blit(cross_img, cross_img.get_rect(center=goal_center))

def vec2int(v):
    return (int(v.x), int(v.y))

def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)
    # return abs(a.x - b.x) ** 2 + abs(a.y - b.y) ** 2

def heuristic_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    path[vec2int(start)] = None

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next in graph.find_neighbors(vec(current)):
            if vec2int(next) not in path:
                priority = heuristic(end, next)
                frontier.put(vec2int(next), priority)
                path[vec2int(next)] = vec(current) - vec(next)
    return path

def dijkstra_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            new_cost = cost[current] + graph.cost(current, next)
            if next not in cost or new_cost < cost[next]:
                cost[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    return path

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
for dir in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
    arrows[dir] = pg.transform.rotate(arrow_img, vec(dir).angle_to(vec(1, 0)))

sg = WeightedGrid(GRIDWIDTH, GRIDHEIGHT)
walls = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (6, 7), (5, 7), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8), (12, 9), (12, 10), (12, 11), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10), (19, 10), (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6), (14, 0), (14, 1), (9, 2), (9, 1), (7, 3), (8, 3), (10, 3), (9, 3), (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11), (1, 11), (2, 11), (21, 2), (20, 11), (20, 12), (23, 13), (23, 14), (24, 10), (25, 10), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (5, 3), (6, 3), (5, 4)]
for wall in walls:
    sg.walls.append(vec(wall))
sg.walls = []

terrain = [(11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (16, 8), (15, 8), (14, 8), (13, 8), (12, 8), (11, 8), (10, 8), (11, 9), (12, 9), (13, 9), (14, 9), (15, 9), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (12, 11), (13, 11), (14, 11), (12, 5), (13, 5), (14, 5), (11, 5), (15, 5), (12, 4), (13, 4), (14, 4)]
terrain = []
for tile in terrain:
    sg.weights[tile] = 15

goal = vec(14, 8)
start = vec(20, 0)
search_type = dijkstra_search
# p = dijkstra_search(sg, goal, start)
# p = heuristic_search(sg, goal, start)
p = search_type(sg, goal, start)

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
                if search_type == dijkstra_search:
                    search_type = heuristic_search
                else:
                    search_type = dijkstra_search
                p = search_type(sg, goal, start)
            if event.key == pg.K_m:
                # dump the wall list for saving
                print([(int(loc.x), int(loc.y)) for loc in sg.walls])
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = vec(pg.mouse.get_pos()) // TILESIZE
            if event.button == 1:
                if mpos in sg.walls:
                    sg.walls.remove(mpos)
                else:
                    sg.walls.append(mpos)
            if event.button == 2:
                start = mpos
            if event.button == 3:
                goal = mpos
            # p, c = dijkstra_search(sg, goal, start)
            p = search_type(sg, goal, start)

    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    # fill explored area
    for node in p:
        x, y = node
        rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, MEDGRAY, rect)
    draw_grid()
    sg.draw()
    # draw path from start to goal
    current = start + p[vec2int(start)]
    l = 1
    while current != goal:
        l += 1
        x = current.x * TILESIZE + TILESIZE / 2
        y = current.y * TILESIZE + TILESIZE / 2
        img = arrows[vec2int(p[(current.x, current.y)])]
        r = img.get_rect(center=(x, y))
        screen.blit(img, r)
        # find next in p
        current = current + p[vec2int(current)]
    draw_icons()
    draw_text(search_type.__name__, 30, WHITE, 10, HEIGHT - 10, align="bottomleft")
    draw_text('Path length:{}'.format(l), 30, WHITE, 10, HEIGHT - 45, align="bottomleft")
    pg.display.flip()
