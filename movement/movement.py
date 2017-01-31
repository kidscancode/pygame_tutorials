import pygame as pg

WIDTH = 1000
HEIGHT = 800
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Movement Example")
clock = pg.time.Clock()

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((64, 64))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.vx, self.vy = 0, 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            self.vy = -5
        if keystate[pg.K_DOWN]:
            self.vy = 5
        if keystate[pg.K_LEFT]:
            self.vx = -2
        if keystate[pg.K_RIGHT]:
            self.vx = 1
        if self.vx != 0 and self.vy != 0:
            self.vx /= 1.414
            self.vy /= 1.414
        self.rect.x += self.vx
        self.rect.y += self.vy

all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)
# Game loop
running = True
while running:
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
    pg.display.flip()

pg.quit()
