# pg template - skeleton for a new pg project
import pygame as pg
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('img/playerShip1_orange.png').convert()
        self.image = pg.transform.scale(self.image, (100, 76))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        
all_sprites = pg.sprite.Group()
p1 = Player()
all_sprites.add(p1)
p2 = Player()
all_sprites.add(p2)
p2.rect.x -= 50
p2.rect.y -= 50

def draw_mask(sprite):
    for x in range(sprite.rect.width):
        for y in range(sprite.rect.height):
            if sprite.mask.get_at((x, y)):
                pg.draw.circle(sprite.image, MAGENTA, (x, y), 1)
                
def draw_outline(sprite):
    o = sprite.mask.outline()
    for px in o:
        pg.draw.circle(sprite.image, MAGENTA, px, 1)

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
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                p2.rect.x -= 1
            if event.key == pg.K_RIGHT:
                p2.rect.x += 1
            if event.key == pg.K_UP:
                p2.rect.y -= 1
            if event.key == pg.K_DOWN:
                p2.rect.y += 1

    # Update
    all_sprites.update()
    # h = pg.sprite.collide_mask(p1, p2)
    draw_mask(p2)
    draw_mask(p1)
    h = p1.mask.overlap_area(p2.mask, (p1.rect.x-p2.rect.x, p1.rect.y-p2.rect.y))
    pg.display.set_caption(str(h))
    # Draw / render
    screen.fill((40, 40, 40))
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()
