import pygame as pg
from random import randint, uniform
import pytweening as tween

vec = pg.math.Vector2

# fade in/out
# grow/shrink

class Particle(pg.sprite.Sprite):
    def __init__(self, image, pos, vel, life, gravity, groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = image.copy()
        self.pos = vec(pos)
        self.vel = vel
        self.life = life
        self.gravity = gravity
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, dt):
        self.vel += self.gravity * dt
        self.pos += self.vel * dt
        self.rect.center = self.pos
        self.life -= dt
        if self.life <= 0:
            self.kill()

class Emitter:
    def __init__(self, count):
        self.particle_pool = []
        for i in range(count):
            self.particle_pool.append(Particle())

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    spawn = vec(400, 300)
    all_sprites = pg.sprite.Group()
    size = 8
    circ = pg.Surface((size, size)).convert_alpha()
    circ.fill((0, 0, 0, 0))
    pg.draw.circle(circ, (255, 255, 0), (size // 2, size // 2), size // 2)
    grav = vec(0, 200)

    running = True
    while running:
        pg.display.set_caption("{:.2f}".format(clock.get_fps()))
        dt = clock.tick(60) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_1:
                for i in range(100):
                    Particle(circ, spawn, vec(randint(300, 400), 0).rotate(uniform(-110, -70)), uniform(1, 5), grav, [all_sprites])
            if event.type == pg.MOUSEBUTTONDOWN:
                Particle(circ, spawn, vec(randint(50, 200), 0).rotate(uniform(0, 360)), 2, grav, [all_sprites])
        all_sprites.update(dt)
        keys = pg.key.get_pressed()
        if keys[pg.K_s]:
            for i in range(10):
                Particle(circ, spawn + vec(0, 250), vec(randint(250, 350), 0).rotate(uniform(-110, -70)), uniform(1, 4), grav, [all_sprites])
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pg.display.flip()

    pg.quit()
