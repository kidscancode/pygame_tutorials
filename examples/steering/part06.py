# Steering Behavior Examples
# Avoid (obstacles) - rect instead of radius
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

# Mob properties
MOB_SIZE = 16
MAX_SPEED = 4
MAX_FORCE = 0.3
WALL_LIMIT = 30
LOOK_AHEAD = 20

class Wall(pg.sprite.Sprite):
    def __init__(self, x=0, y=0, w=32, h=32):
        self.groups = all_sprites, walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w, h))
        self.image.fill(LIGHTGRAY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collide_rect = self.rect.inflate(WALL_LIMIT, WALL_LIMIT)

    def draw_vectors(self):
        pg.draw.rect(screen, CYAN, self.collide_rect, 2)


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

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def find_collision(self, group, ahead, ahead2):
        for obs in group:
            if obs.collide_rect.collidepoint(ahead) or obs.collide_rect.collidepoint(ahead2):
                return obs
        return None

    def avoid_obstacles(self, group):
        dyn_length = LOOK_AHEAD * self.vel.length() / MAX_SPEED
        ahead = self.pos + self.vel.normalize() * dyn_length
        ahead2 = self.pos + self.vel.normalize() * dyn_length / 2
        self.a = vec(ahead)
        self.a2 = vec(ahead2)
        hit = self.find_collision(group, ahead, ahead2)
        if hit:
            desired = self.vel.normalize() * MAX_SPEED
            if self.pos.x < hit.rect.right and self.pos.x > hit.rect.left:
                if self.pos.y > hit.rect.bottom:
                    desired = vec(self.vel.x, MAX_SPEED)
                if self.pos.y < hit.rect.top:
                    desired = vec(self.vel.x, -MAX_SPEED)
            if self.pos.y < hit.rect.bottom and self.pos.y > hit.rect.top:
                if self.pos.x > hit.rect.right:
                    desired = vec(MAX_SPEED, self.vel.y)
                if self.pos.x < hit.rect.left:
                    desired = vec(-MAX_SPEED, self.vel.y)
            steer = desired - self.vel
            if steer.length_squared() > 0:
                steer.normalize_ip()
                steer.scale_to_length(MAX_FORCE)
        else:
            steer = vec(0, 0)
        self.steer = steer
        return steer

    def update(self):
        self.acc = self.avoid_obstacles(walls) * 2
        self.acc += self.seek(pg.mouse.get_pos())
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
        # steer
        pg.draw.line(screen, MAGENTA, self.pos, (self.pos + self.steer * scale * 5), 5)
        # ahead
        ax = int(self.a.x)
        ay = int(self.a.y)
        pg.draw.circle(screen, CYAN, (ax, ay), 5)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
walls = pg.sprite.Group()
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

for i in range(10):
    randwall()

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

    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    all_sprites.draw(screen)
    if show_vectors:
        for sprite in all_sprites:
            sprite.draw_vectors()
    pg.display.flip()
