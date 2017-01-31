# Steering Behavior Examples
# Testing SteeringManager
# KidsCanCode 2016
import pygame as pg
from random import randint, uniform
from SteeringManager import *
vec = pg.math.Vector2

WIDTH = 1000
HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)

# Mob properties
MOB_SIZE = 16
MOB_BEHAVIORS = {'max_force': 0.2,
                 'max_speed': 5,
                 'seek_radius': 300,
                 'flee_radius': 400,
                 'wall_limit': 80,
                 'wander_ring_radius': 50,
                 'wander_ring_distance': 150,
                 'neighbor_radius': 50,
                 'sep_weight': 1.5,
                 'ali_weight': 0.8,
                 'coh_weight': 1}

def draw_text(text, size, color, x, y, align="topleft"):
    font_name = pg.font.match_font('hack')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    screen.blit(text_surface, text_rect)

class Predator(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(25, WIDTH - 25), randint(25, HEIGHT - 25))
        self.vel = vec(3, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.steering = SteeringManager(self)

    def update(self):
        # self.steering.seek(pg.mouse.get_pos())
        self.steering.wander()
        self.steering.avoid_walls()
        self.steering.update()

        self.rect.center = self.pos

class Mob(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites, mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.behaviors = MOB_BEHAVIORS
        self.image = pg.Surface((MOB_SIZE, MOB_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(0, WIDTH), randint(0, HEIGHT))
        self.vel = vec(self.behaviors['max_speed'], 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.steering = SteeringManager(self)

    def update(self):
        self.steering.seek(pg.mouse.get_pos())
        # self.steering.evade(p1.pos, 2.0)
        self.steering.wander()
        self.steering.flock(mobs)
        # self.steering.avoid_walls(screen.get_rect(), 2)
        self.steering.update()
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        self.rect.center = self.pos

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
m = Mob()
# p1 = Predator()
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
    # draw_text(str(m.steering.steering), 18, WHITE, 5, 5)
    # draw_text(str(m.acc), 18, WHITE, 5, 25)
    # draw_text(str(m.vel.length()), 18, WHITE, 5, 45)
    if show_vectors:
        for sprite in all_sprites:
            sprite.steering.draw_vectors(screen)
    pg.display.flip()
