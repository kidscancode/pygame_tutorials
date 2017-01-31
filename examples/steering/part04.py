# Steering Behavior Examples
# Wall avoid
# KidsCanCode 2016
import pygame as pg
from random import randint, uniform
vec = pg.math.Vector2

WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)

# Mob properties
MOB_SIZE = 32
MAX_SPEED = 4
MAX_FORCE = 0.2
WALL_LIMIT = 50

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

    def avoid_walls(self):
        steer = vec(0, 0)
        self.desired = vec(0, 0)
        near_wall = False
        if self.pos.x < WALL_LIMIT:
            self.desired = vec(MAX_SPEED, self.vel.y)
            near_wall = True
        if self.pos.x > WIDTH - WALL_LIMIT:
            self.desired = vec(-MAX_SPEED, self.vel.y)
            near_wall = True
        if self.pos.y < WALL_LIMIT:
            self.desired = vec(self.vel.x, MAX_SPEED)
            near_wall = True
        if self.pos.y > HEIGHT - WALL_LIMIT:
            self.desired = vec(self.vel.x, -MAX_SPEED)
            near_wall = True
        if near_wall:
            steer = (self.desired - self.vel)
            if steer.length() > MAX_FORCE:
                steer.scale_to_length(MAX_FORCE)
        return steer

    def update(self):
        self.acc = self.avoid_walls()
        # equations of motion
        self.vel += self.acc
        if self.acc.length() == 0:
            self.vel.scale_to_length(MAX_SPEED)
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
        if self.pos.y < 0:
            self.pos.y = 0
        self.rect.center = self.pos

    def draw_vectors(self):
        scale = 25
        # vel
        pg.draw.line(screen, GREEN, self.pos, (self.pos + self.vel * scale), 5)
        # desired
        pg.draw.line(screen, RED, self.pos, (self.pos + self.desired * scale), 5)
        # limits
        r = pg.Rect(WALL_LIMIT, WALL_LIMIT, WIDTH - WALL_LIMIT * 2, HEIGHT - WALL_LIMIT * 2)
        pg.draw.rect(screen, WHITE, r, 1)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
Mob()
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

    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    all_sprites.draw(screen)
    if show_vectors:
        for sprite in all_sprites:
            sprite.draw_vectors()
    pg.display.flip()
