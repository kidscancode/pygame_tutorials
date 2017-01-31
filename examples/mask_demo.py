# quick demo to help explain masks and pixel perfect collisions
import pygame as pg

WIDTH = 480
HEIGHT = 480
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

def draw_text(text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

ship_image = pg.image.load('playerShip1_orange.png').convert_alpha()
ship_image = pg.transform.scale(ship_image, (200, 76 * 2))
bunny_image = pg.image.load('bunny1_ready.png').convert_alpha()
enemy_image = pg.image.load('flyMan_fly.png').convert_alpha()
class Player(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

all_sprites = pg.sprite.Group()
p1 = Player(bunny_image)
all_sprites.add(p1)
p2 = Player(enemy_image)
all_sprites.add(p2)
p2.rect.x -= 125
p2.rect.y -= 125

def draw_mask(sprite):
    # fill the sprite's mask
    for x in range(sprite.rect.width):
        for y in range(sprite.rect.height):
            if sprite.mask.get_at((x, y)):
                pg.draw.circle(sprite.image, MAGENTA, (x, y), 1)

def draw_outline(sprite):
    # outline the sprite's mask
    o = sprite.mask.outline()
    for px in o:
        pg.draw.circle(sprite.image, MAGENTA, px, 2)

# Game loop
running = True
outline_on = False
fill_on = False
pg.key.set_repeat(200, 50)
while running:
    clock.tick(FPS)
    for event in pg.event.get():
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
            if event.key == pg.K_m:
                fill_on = not fill_on
                outline_on = False
            if event.key == pg.K_o:
                outline_on = not outline_on
                fill_on = False

    # Update
    all_sprites.update()
    h = pg.sprite.collide_mask(p1, p2)
    if outline_on:
        draw_outline(p2)
        draw_outline(p1)
    elif fill_on:
        draw_mask(p2)
        draw_mask(p1)
    elif not outline_on and not fill_on:
        p1.image = bunny_image.copy()
        p2.image = enemy_image.copy()
    # h = p1.mask.overlap_area(p2.mask, (p1.rect.x-p2.rect.x, p1.rect.y-p2.rect.y))
    # pg.display.set_caption(str(h))

    screen.fill((40, 40, 40))
    screen.blit(p1.image, p1.rect)
    pg.draw.rect(screen, WHITE, p1.rect, 1)
    pg.draw.rect(screen, WHITE, p2.rect, 1)
    screen.blit(p2.image, p2.rect)
    draw_text("Hit: " + str(h), 18, WHITE, WIDTH / 2, 5)
    if h:
        px = (h[0] + p1.rect.x, h[1] + p1.rect.y)
        pg.draw.circle(screen, CYAN, px, 4)
    pg.display.flip()

pg.quit()
