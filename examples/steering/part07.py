# Steering Behavior Examples
# Flow field
# KidsCanCode 2016
import pygame as pg
from random import randint, uniform
vec = pg.math.Vector2

WIDTH = 800
HEIGHT = 640
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

TILESIZE = 32
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE
# Mob properties
MOB_SIZE = 16
MAX_SPEED = 4
MAX_FORCE = 0.1

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

# def make_field(v=vec(1, 1)):
#     field = {}
#     for x in range(0, GRIDWIDTH + 1):
#         for y in range(0, GRIDHEIGHT + 1):
#             field[(x, y)] = v
#     return field
#
# CENTER ATTRACTOR:
# dist = vec(x * TILESIZE, y * TILESIZE) - vec(WIDTH / 2, HEIGHT / 2)
# a = (WIDTH // 2 - x) * 2
# dist = dist.rotate(a)
# field[(x, y)] = -dist.normalize()

def make_field():
    field = {}
    for x in range(0, GRIDWIDTH + 1):
        for y in range(0, GRIDHEIGHT + 1):
            dist = vec(x * TILESIZE, y * TILESIZE) - vec(WIDTH / 2, HEIGHT / 2)
            a = (WIDTH // 2 - x) * 2
            dist = dist.rotate(a)
            field[(x, y)] = -dist.normalize()
    return field

def make_rand_field():
    field = {}
    for x in range(0, GRIDWIDTH + 1):
        for y in range(0, GRIDHEIGHT + 1):
            field[(x, y)] = vec(1, 0).rotate(uniform(0, 360))
    return field

def generate_field():
    field = {}
    for x in range(0, GRIDWIDTH + 1):
        for y in range(0, GRIDHEIGHT + 1):
            field[(x, y)] = vec(1, 0)
    for wall in walls:
        wallpos = vec(wall.rect.x // TILESIZE, wall.rect.y // TILESIZE)
        field[(wallpos.x, wallpos.y)] = vec(0, 0)
        if wallpos.x - 1 >= 0:
            field[(wallpos.x - 1, wallpos.y)] = vec(0, -1)
        if wallpos.x + 1 <= GRIDWIDTH:
            field[(wallpos.x + 1, wallpos.y)] = vec(0, 1)
        if wallpos.y - 1 >= 0:
            field[(wallpos.x, wallpos.y - 1)] = vec(1, 0)
        if wallpos.y + 1 <= GRIDHEIGHT:
            field[(wallpos.x, wallpos.y + 1)] = vec(-1, 0)
    return field

def field_adjust(field):
    wall_list = []
    for wall in walls:
        wallpos = (wall.rect.x // TILESIZE, wall.rect.y // TILESIZE)
        wall_list.append(wallpos)
    for x in range(0, GRIDWIDTH + 1):
        for y in range(0, GRIDHEIGHT + 1):
            if (x, y) in wall_list:
                field[(x, y)] = vec(0, 0)
            else:
                dist = vec(x * TILESIZE, y * TILESIZE) - vec(WIDTH / 2, HEIGHT / 2)
                a = (WIDTH // 2 - x) * 2
                dist = dist.rotate(a)
                field[(x, y)] = -dist.normalize()
    return field

def draw_field(field):
    for x in range(0, GRIDWIDTH):
        for y in range(0, GRIDHEIGHT):
            sx = x * TILESIZE + TILESIZE / 2
            sy = y * TILESIZE + TILESIZE / 2
            ex = sx + field[(x, y)].x * 10
            ey = sy + field[(x, y)].y * 10
            pg.draw.line(screen, MAGENTA, (sx, sy), (ex, ey), 1)

class Wall(pg.sprite.Sprite):
    def __init__(self, x=0, y=0, w=32, h=32):
        self.groups = all_sprites, walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w, h))
        self.image.fill(LIGHTGRAY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

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
        desired = field[gridpos] * MAX_SPEED
        if desired.length_squared() > 0:
            steer = desired - self.vel
            if steer.length() > MAX_FORCE:
                steer.scale_to_length(MAX_FORCE)
        return steer

    def update(self):
        self.acc = self.follow_field(field)
        # equations of motion
        self.vel += self.acc
        if self.acc.length() == 0:
            self.vel.scale_to_length(MAX_SPEED)
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        self.rect.center = self.pos

    def draw_vectors(self):
        scale = 25
        # vel
        pg.draw.line(screen, GREEN, self.pos, (self.pos + self.vel * scale), 5)
        # desired
        pg.draw.line(screen, RED, self.pos, (self.pos + self.acc * scale * 5), 5)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
walls = pg.sprite.Group()
field = generate_field()
Mob()

def randwall():
    x = randint(0, WIDTH / 32)
    y = randint(0, HEIGHT / 32)
    w = randint(1, 3) * 32
    h = randint(1, 3) * 32
    Wall(x=x * 32, y=y * 32, w=w, h=h)

def randwall_sq():
    x = randint(0, WIDTH / 32)
    y = randint(0, HEIGHT / 32)
    Wall(x=x * 32, y=y * 32, w=32, h=32)


paused = False
show_vectors = False
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
            if event.key == pg.K_v:
                show_vectors = not show_vectors
            if event.key == pg.K_m:
                Mob()
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = pg.mouse.get_pos()
            x = mpos[0] // 32
            y = mpos[1] // 32
            if event.button == 1:
                Wall(x=x * 32, y=y * 32)
            if event.button == 3:
                for sprite in all_sprites:
                    if sprite.rect.collidepoint(mpos):
                        sprite.kill()
            field = generate_field()

    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    draw_grid()
    all_sprites.draw(screen)
    if show_vectors:
        for sprite in all_sprites:
            sprite.draw_vectors()
        draw_field(field)
    pg.display.flip()
