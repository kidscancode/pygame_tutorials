# pg template - skeleton for a new pg project
import pygame as pg
from math import atan2, cos, sin

WIDTH = 800
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Vector Basics")
clock = pg.time.Clock()
vec = pg.math.Vector2

class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        a = (pg.mouse.get_pos() - player.pos).angle_to(vec(1, 0))
        self.pos = player.pos + vec(50, 0).rotate(-a)
        self.vel = vec(400, 0).rotate(-a)
        self.spawn_time = pg.time.get_ticks()

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > 2000:
            self.kill()

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.rect.center = self.pos

    def update(self, dt):
        # pass
        self.move_to_mouse(dt)
        # self.move_to_mouse_no_vector(dt)
        # self.angle_to_mouse(dt)

    def angle_to_mouse(self, dt):
        d = pg.mouse.get_pos() - self.pos
        a = d.angle_to(vec(1, 0))
        pg.display.set_caption(str(a))

    def move_to_mouse(self, dt):
        mpos = pg.mouse.get_pos()
        # self.vel = (mpos - self.pos).normalize() * 5
        self.vel = (mpos - self.pos) * 0.1 * 25
        # if (mpos - self.pos).length() > 5:
        self.pos += self.vel * dt
        self.rect.center = self.pos

    def move_to_mouse_no_vector(self, dt):
        mpos = pg.mouse.get_pos()
        dx = mpos[0] - self.rect.centerx
        dy = mpos[1] - self.rect.centery
        a = atan2(dy, dx)
        vx = 500 * cos(a)
        vy = 500 * sin(a)
        if (dx**2 + dy**2) > 15:
            self.rect.centerx += vx * dt
            self.rect.centery += vy * dt

all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    dt = clock.tick(FPS) / 1000
    # Process input (events)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            b = Bullet(player)
            all_sprites.add(b)
    # Update
    all_sprites.update(dt)
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # pg.draw.line(screen, WHITE, player.pos, pg.mouse.get_pos(), 2)
    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()
