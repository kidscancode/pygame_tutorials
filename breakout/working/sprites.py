# Sprite classes for platform game
import pygame as pg
from random import randrange, choice
from settings import *
vec = pg.math.Vector2

class Paddle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 30)
        self.pos = vec(WIDTH / 2, HEIGHT - 30)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.update_acc()

    def update_abs(self):
        # absolute position - paddle follows mouse
        pos = pg.mouse.get_pos()
        self.pos.x = pos[0]
        if self.pos.x > WIDTH - PADDLE_WIDTH / 2:
            self.pos.x = WIDTH - PADDLE_WIDTH / 2
        if self.pos.x < PADDLE_WIDTH / 2:
            self.pos.x = PADDLE_WIDTH / 2
        self.rect.center = self.pos

    def update_acc(self):
        # paddle accelerates towards mouse
        self.acc = vec(0, 0)
        pos = pg.mouse.get_pos()
        if abs(pos[0] - self.pos.x) < 50:
            self.acc = vec(0, 0)
        elif pos[0] < self.pos.x:
            self.acc.x = -PADDLE_ACC
        elif pos[0] > self.pos.x:
            self.acc.x = PADDLE_ACC

        self.acc.x += self.vel.x * PADDLE_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > WIDTH - PADDLE_WIDTH / 2:
            self.pos.x = WIDTH - PADDLE_WIDTH / 2
        if self.pos.x < PADDLE_WIDTH / 2:
            self.pos.x = PADDLE_WIDTH / 2
        self.rect.center = self.pos

class Ball(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.speed = BALL_SPEED
        self.image = pg.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(BALL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(choice([-2, -1, 1, 2]), -1)
        self.vel = self.vel.normalize() * self.speed

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vel.x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vel.y *= -1

class Brick(pg.sprite.Sprite):
    def __init__(self, x, y, col):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
