# Introducing vectors and some ways to use them
# Improving movement accuracy
import pygame as pg

WIDTH = 600
HEIGHT = 600
FPS = 60
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Non-integer movement Example")
clock = pg.time.Clock()

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx = 120  # pixels per second
        self.px = 0
        self.rect.left = 0
        self.rect.centery = HEIGHT / 2

    def update(self, dt):
        self.px += self.vx * dt  # time-based movement
        if self.px > WIDTH:
            self.px = 0
        self.rect.x = self.px

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
    # Update
    player.update(dt)
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()
