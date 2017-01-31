import pygame as pg
from random import randint
vec = pg.math.Vector2

WIDTH = 900
HEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (255, 255, 255)
DARKGRAY = (55, 55, 55)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)

# mob properties
MAX_SPEED = 6
MAX_FORCE = 0.1
APPROACH_RADIUS = 100
SEPARATION = 20
SEEK_WEIGHT = 1
AVOID_WEIGHT = 3.5

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

class Mob(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((16, 16))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(25, WIDTH - 25), randint(25, HEIGHT - 25))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.steer = vec(0, 0)

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        self.steer = (self.desired - self.vel)
        if self.steer.length() > MAX_FORCE:
            self.steer.scale_to_length(MAX_FORCE)

    def seek_with_approach(self, target):
        self.desired = (target - self.pos) * 0.1
        if self.desired.length() > MAX_SPEED:
            self.desired.scale_to_length(MAX_SPEED)
        self.steer = (self.desired - self.vel)
        if self.steer.length() > MAX_FORCE:
            self.steer.scale_to_length(MAX_FORCE)

    def seek_with_approach2(self, target):
        # more intelligent slowing
        desired = (target - self.pos)
        d = desired.length()
        desired.normalize_ip()
        if d < APPROACH_RADIUS:
            desired *= d / APPROACH_RADIUS * MAX_SPEED
        else:
            desired *= MAX_SPEED
        steer = (desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def separate(self):
        # move away from other mobs
        desired = vec(0, 0)
        steer = vec(0, 0)
        count = 0
        for mob in all_sprites:
            if mob != self:
                d = self.pos.distance_to(mob.pos)
                if d < SEPARATION:
                    diff = (self.pos - mob.pos).normalize()
                    desired += diff
                    count += 1
        if count > 0:
            desired /= count
            desired.scale_to_length(MAX_SPEED)
            steer = (desired - self.vel)
            if steer.length() > MAX_FORCE:
                steer.scale_to_length(MAX_FORCE)
        return steer

    def update(self):
        mpos = vec(pg.mouse.get_pos())
        seek = self.seek_with_approach2(mpos)
        self.vel += seek * SEEK_WEIGHT
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        avoid = self.separate() * AVOID_WEIGHT
        self.vel += avoid
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        self.rect.center = self.pos

def draw_vectors():
    for mob in all_sprites:
        # vel vector
        draw_arrow(mob.pos, (mob.pos + mob.vel * 45), GREEN, 5)
        # desired vector
        draw_arrow(mob.pos, (mob.pos + mob.desired * 45), RED, 5)
        # steer vector
        draw_arrow((mob.pos + mob.vel * 45),
                   (mob.pos + mob.vel * 45) + mob.steer * 300,
                   CYAN, 5)

def draw_arrow(p1, p2, col, size):
    # line portion
    pg.draw.line(screen, col, p1, p2, size)

all_sprites = pg.sprite.Group()
Mob()
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
            if event.key == pg.K_v:
                show_vectors = not show_vectors
            if event.key == pg.K_SPACE:
                Mob()
        if event.type == pg.MOUSEBUTTONDOWN:
            r = pg.Rect(0, 0, 10, 10)
            r.center = pg.mouse.get_pos()
            for m in all_sprites:
                if m.rect.collidepoint(r.center):
                    m.kill()

    all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    all_sprites.draw(screen)
    pg.draw.circle(screen, WHITE, pg.mouse.get_pos(), APPROACH_RADIUS, 2)
    if show_vectors:
        draw_vectors()
    pg.display.flip()

pg.quit()
