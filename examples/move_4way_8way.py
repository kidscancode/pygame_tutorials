# pg template - skeleton for a new pg project
import pygame as pg

WIDTH = 800
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
pg.display.set_caption("4-way vs. 8-way Movement")
clock = pg.time.Clock()

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.vx, self.vy = 0, 0
        self.move_8way_fixdiag()
        self.rect.x += self.vx
        self.rect.y += self.vy
        # prevent sprite from moving off screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def move_4way(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            self.vy = -5
        elif keystate[pg.K_DOWN]:
            self.vy = 5
        elif keystate[pg.K_LEFT]:
            self.vx = -5
        elif keystate[pg.K_RIGHT]:
            self.vx = 5

    def move_8way(self):
        self.vx, self.vy = 0, 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            self.vy += -5
        if keystate[pg.K_DOWN]:
            self.vy += 5
        if keystate[pg.K_LEFT]:
            self.vx += -5
        if keystate[pg.K_RIGHT]:
            self.vx += 5

    def move_8way_fixdiag(self):
        self.move_8way()
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)

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
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()
