# Steering Behavior Examples
# Flow field pathfinding
# KidsCanCode 2016
import pygame as pg
from random import randint, uniform
# from queue import Queue
import collections
vec = pg.math.Vector2

class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, item):
        self.elements.append(item)

    def get(self):
        return self.elements.popleft()

def vec_t(v):
    return (int(v.x), int(v.y))

TILESIZE = 64
GRIDWIDTH = 25
GRIDHEIGHT = 12
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
# WIDTH = 1200
# HEIGHT = 800
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

SEARCH_RANGE = 700
# Mob properties
MOB_SIZE = 16
MAX_SPEED = 4
MAX_FORCE = 0.5

font_name = pg.font.match_font('hack')
def draw_text(text, size, color, x, y, align="nw"):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color).convert_alpha()
    text_rect = text_surface.get_rect()
    if align == "nw":
        text_rect.topleft = (x, y)
    if align == "ne":
        text_rect.topright = (x, y)
    if align == "sw":
        text_rect.bottomleft = (x, y)
    if align == "se":
        text_rect.bottomright = (x, y)
    if align == "n":
        text_rect.midtop = (x, y)
    if align == "s":
        text_rect.midbottom = (x, y)
    if align == "e":
        text_rect.midright = (x, y)
    if align == "w":
        text_rect.midleft = (x, y)
    if align == "center":
        text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

def color_gradient(c1, c2, d):
    r = c1[0] + (c2[0] - c1[0]) * d
    g = c1[1] + (c2[1] - c1[1]) * d
    b = c1[2] + (c2[2] - c1[2]) * d
    return (r, g, b)

class Player(pg.sprite.Sprite):
    def __init__(self):
        groups = all_sprites
        pg.sprite.Sprite.__init__(self, groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.rect.center = self.pos

    def update(self):
        self.vel = vec(0, 0)
        self.move_8way()
        self.pos += self.vel
        self.rect.center = self.pos
        # prevent sprite from moving off screen
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT

    def move_8way(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            self.vel.y = -5
        if keystate[pg.K_DOWN]:
            self.vel.y = 5
        if keystate[pg.K_LEFT]:
            self.vel.x = -5
        if keystate[pg.K_RIGHT]:
            self.vel.x = 5

    def draw_vectors(self):
        pass

class FlowField:
    def __init__(self):
        self.empty_field = {}
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        self.generate()
        self.vec_image = pg.image.load("arrowRight.png").convert_alpha()
        self.vec_image = pg.transform.scale(self.vec_image, (int(TILESIZE * 0.6), int(TILESIZE * 0.6)))
        self.vec_images = {}
        for angle in [0, 45, -45, 90, -90, 135, -135, -180]:
            self.vec_images[angle] = pg.transform.rotate(self.vec_image.copy(), angle)

    def generate(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.empty_field[(x, y)] = vec(0, 0)

    def remove_walls(self):
        for wall in walls:
            # self.field[(wall.x, wall.y)] = None
            if (wall.x, wall.y) in self.field:
                self.field.pop((wall.x, wall.y))

    def heuristic(self, a, b):
        # manhattan distance
        return abs(a.x - b.x) + abs(a.y - b.y)

    def fill(self, start):
        self.field = self.empty_field.copy()
        self.remove_walls()
        frontier = Queue()
        start = vec_t(start)
        frontier.put(start)
        came_from = {}
        self.distance = {}
        # self.max_distance = 0
        came_from[start] = None
        # self.distance[start] = 0
        while not frontier.empty():
            current = frontier.get()
            for next in self.find_neighbors(current, self.field):
                if next not in came_from:
                    # priority = self.heuristic(goal, next)
                    frontier.put(next)
                    came_from[next] = current
                    # self.distance[next] = 1 + self.distance[current]
                    # if self.distance[next] > self.max_distance:
                    #     self.max_distance = self.distance[next]
                    self.field[next] = vec(current) - vec(next)

    def fill2(self, start, rect):
        self.field = self.empty_field.copy()
        searches = self.cells_for_rect(rect)
        # print(list(searches))
        sub_field = {}
        for c in searches:
            if c in self.field.keys():
                sub_field[c] = self.field[c]
        frontier = Queue()
        start = vec_t(start)
        frontier.put(start)
        came_from = {}
        self.distance = {}
        self.max_distance = 0
        came_from[start] = None
        self.distance[start] = 0
        while not frontier.empty():
            current = frontier.get()
            for next in self.find_neighbors(current, sub_field):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current
                    self.distance[next] = 1 + self.distance[current]
                    if self.distance[next] > self.max_distance:
                        self.max_distance = self.distance[next]
                    self.field[next] = vec(current) - vec(next)

    def cells_for_rect(self, rect):
        x1 = rect.x // TILESIZE
        y1 = rect.y // TILESIZE
        x2 = rect.right // TILESIZE
        y2 = rect.bottom // TILESIZE
        cells = ((x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1))
        return cells

    def find_neighbors(self, loc, field):
        neighbors = []
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        # if (loc.x + loc.y) % 2 == 0:
        #     directions.reverse()
        for direction in directions:
            neighbor = (loc[0] + direction[0], loc[1] + direction[1])
            if neighbor in field:
                # if self.field[(int(neighbor.x), int(neighbor.y))] is not None:
                neighbors.append(neighbor)
        # print("N: " + str(neighbors))
        return neighbors

    def draw(self):
        show_arrow = True
        show_dist = False
        for pos, v in self.field.items():
            if v.length_squared() > 0:
                if show_dist:
                    start_color = (200, 50, 0)
                    end_color = DARKGRAY
                    p_rect = pg.Rect((p.pos.x // TILESIZE) * TILESIZE, (p.pos.y // TILESIZE) * TILESIZE, TILESIZE, TILESIZE)
                    pg.draw.rect(screen, start_color, p_rect)
                    rect = pg.Rect(pos[0] * TILESIZE, pos[1] * TILESIZE, TILESIZE, TILESIZE)
                    r = self.distance[pos] / self.max_distance
                    col = color_gradient(start_color, end_color, r)
                    pg.draw.rect(screen, col, rect)
                if show_arrow:
                    rot = v.angle_to(vec(1, 0))
                    img = self.vec_images[rot]
                    rect = img.get_rect()
                    rect.center = (pos[0] * TILESIZE + TILESIZE / 2, pos[1] * TILESIZE + TILESIZE / 2)
                    screen.blit(img, rect)
                    # draw_text(str(self.distance[pos]), 12, WHITE, rect.centerx, rect.centery, align="center")

class Wall(pg.sprite.Sprite):
    def __init__(self, x=0, y=0, w=TILESIZE, h=TILESIZE):
        self.groups = all_sprites, walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = pg.Surface((w, h))
        self.image.fill(LIGHTGRAY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)

    def draw_vectors(self):
        pass

class Mob(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((MOB_SIZE, MOB_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(0, WIDTH), randint(0, HEIGHT))
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos

    def follow_field(self, field):
        steer = vec(0, 0)
        gridpos = self.pos // TILESIZE
        gridpos = (int(gridpos.x), int(gridpos.y))
        if gridpos in field.field:
            desired = field.field[gridpos] * MAX_SPEED
            if desired.length_squared() > 0:
                steer = desired - self.vel
                if steer.length() > MAX_FORCE:
                    steer.scale_to_length(MAX_FORCE)
        return steer

    def update(self):
        if (self.pos - p.pos).length_squared() < SEARCH_RANGE**2:
            self.acc = self.follow_field(field)
        # equations of motion
        self.vel += self.acc
        if self.acc.length() == 0:
            self.vel.scale_to_length(MAX_SPEED)
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        if self.pos.x > WIDTH - 1:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH - 1
        if self.pos.y > HEIGHT - 1:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT - 1
        self.rect.center = self.pos

    def draw_vectors(self):
        scale = 25
        # vel
        pg.draw.line(screen, GREEN, self.pos, (self.pos + self.vel * scale), 5)
        # desired
        pg.draw.line(screen, RED, self.pos, (self.pos + self.acc * scale * 5), 5)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF | pg.HWSURFACE)
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
walls = pg.sprite.Group()
p = Player()
# Mob()
for y in [8, 9, 10, 11]:
    Wall(x=10, y=y, w=TILESIZE, h=TILESIZE)
field = FlowField()

paused = False
show_vectors = False
last_update = 0
running = True
while running:
    clock.tick(FPS)
    now = pg.time.get_ticks()
    if now - last_update > 500:
        last_update = now
        # field.generate()
        field.fill(vec(p.pos.x // TILESIZE, p.pos.y // TILESIZE))
        # field.fill2(vec(p.pos.x // TILESIZE, p.pos.y // TILESIZE), p.rect.inflate(SEARCH_RANGE, SEARCH_RANGE))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                paused = not paused
            if event.key == pg.K_v:
                show_vectors = not show_vectors
            if event.key == pg.K_m:
                Mob()
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = pg.mouse.get_pos()
            x = mpos[0] // TILESIZE
            y = mpos[1] // TILESIZE
            if event.button == 1:
                Wall(x=x, y=y)
            if event.button == 3:
                for wall in walls:
                    if wall.rect.collidepoint(mpos):
                        wall.kill()

    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    if show_vectors:
        field.draw()
    # draw_grid()
    all_sprites.draw(screen)
    if show_vectors:
        for sprite in all_sprites:
            sprite.draw_vectors()
    pg.display.flip()
