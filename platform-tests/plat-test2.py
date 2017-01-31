# Platform game tutorial

import pygame as pg
import random

WIDTH = 600
HEIGHT = 480
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 155, 155)

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.acc = pg.math.Vector2(0, 0)
        self.vel = pg.math.Vector2(0, 0)
        self.pos = pg.math.Vector2(200, HEIGHT - 100)
        # pos will be bottom center of sprite
        self.jumping = False
        self.rect.midbottom = (self.pos)

    def get_keys(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.acc.x = -1
        if keystate[pg.K_RIGHT]:
            self.acc.x = 1

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.acc.y = -5
            self.jumping = True

    def check_collisions(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, platforms, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width / 2
                    self.rect.right = hits[0].rect.left
                elif self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.rect.width / 2
                    self.rect.left = hits[0].rect.right
                self.vel.x = 0
        elif dir == 'y':
            hits = pg.sprite.spritecollide(self, platforms, False)
            for hit in hits:
                if self.vel.y > 0:
                    self.pos.y = hit.rect.top
                    self.vel.x += hit.vx
                elif self.vel.y < 0:
                    self.pos.y = hit.rect.bottom + self.rect.height
                self.vel.y = 0
                self.jumping = False

    def update(self):
        self.acc = pg.math.Vector2(0, 1)
        self.get_keys()
        # add friction (l/r)
        self.acc.x += self.vel.x * -0.18
        self.vel += self.acc
        self.pos += self.vel
        self.rect.bottom = self.pos.y
        self.check_collisions('y')
        self.rect.centerx = self.pos.x
        self.check_collisions('x')
        # if self.rect.right > WIDTH:
        #     self.px = WIDTH - self.rect.width / 2
        #     self.vx = 0
        #     self.rect.right = WIDTH
        # if self.rect.left < 0:
        #     self.px = self.rect.width / 2
        #     self.vx = 0
        #     self.rect.left = 0

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, vx, vy):
        super(Platform, self).__init__()
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.vx *= -1

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
platforms = pg.sprite.Group()
player = Player()
all_sprites.add(player)
p_list = [[-100, HEIGHT - 20, WIDTH + 100, 20, 0, 0],
          [WIDTH / 2, HEIGHT - 150, 100, 20, 0, 0],
          [WIDTH / 2 + 80, HEIGHT - 300, 20, 150, 0, 0],
          [0, HEIGHT - 320, 75, 20, 2, 0],
          [0, HEIGHT - 100, 75, 20, 2.1, 0]]
for loc in p_list:
    plat = Platform(loc[0], loc[1], loc[2], loc[3], loc[4], loc[5])
    all_sprites.add(plat)
    platforms.add(plat)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                player.jump_cut()

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(LIGHTBLUE)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()
