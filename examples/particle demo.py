import pygame as pg
from random import uniform, choice
vec = pg.math.Vector2

class Particle(pg.sprite.Sprite):
    def __init__(self, groups, image, pos, lifetime=1000, speed_max=50, speed_min=10, fade_start=0, gravity=0):
        pg.sprite.Sprite.__init__(self, groups)
        self.image = image.copy()
        self.pos = vec(pos)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.vel = vec(uniform(speed_min, speed_max), 0).rotate(uniform(0, 360))
        self.lifetime = lifetime
        self.age = 0
        self.fade_start = fade_start
        self.gravity = gravity

    def update(self, dt):
        self.shrink()
        self.fade()
        self.vel.y += self.gravity
        self.pos += self.vel * dt
        self.rect.center = self.pos
        self.age += dt * 1000
        if self.age > self.lifetime:
            self.kill()

    def shrink(self):
        if self.age > self.fade_start:
            try:
                ratio = (self.age - self.fade_start) / (self.lifetime - self.fade_start)
            except ZeroDivisionError:
                ratio = 1
            if ratio > 1:
                ratio = 1
            scale = 1 - ratio
            self.image = pg.transform.rotozoom(img.copy(), 0, ratio)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
    # def blit(self, surface):
    #     return surface.blit(self.image, self.rect, special_flags=pg.BLEND_RGB_SUB)

    def fade(self):
        if self.age > self.fade_start:
            try:
                ratio = (self.age - self.fade_start) / (self.lifetime - self.fade_start)
            except ZeroDivisionError:
                ratio = .5
            if ratio > .5:
                ratio = .5
            mask = int(255 * (1 - ratio))
            self.image.fill([mask, mask, mask], special_flags=pg.BLEND_RGBA_MIN)

pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

# img = pg.image.load('blackSmoke00.png').convert_alpha()
# img = pg.transform.rotozoom(img, 0, .15)
puffs = []
for i in range(25):
    img = pg.image.load('whitePuff{:02}.png'.format(i)).convert_alpha()
    img = pg.transform.rotozoom(img, 0, .2)
    puffs.append(img)

running = True
all_sprites = pg.sprite.Group()
while running:
    dt = clock.tick(60) / 1000
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            running = False
        if e.type == pg.MOUSEBUTTONDOWN:
            for i in range(20):
                Particle(all_sprites, choice(puffs), e.pos)

    all_sprites.update(dt)

    screen.fill((120, 120, 120))
    all_sprites.draw(screen)
    pg.display.flip()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))

pg.quit()
