# pg template - skeleton for a new pg project
import pygame as pg
vec = pg.math.Vector2

WIDTH = 1000
HEIGHT = 800
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

def draw_text(text, size, color, x, y, align="nw"):
    font_name = pg.font.match_font('hack')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "nw":
        text_rect.topleft = (x, y)
    if align == "ne":
        text_rect.topright = (x, y)
    if align == "sw":
        text_rect.bottomleft = (x, y)
    if align == "se":
        text_rect.bottomright = (x, y)
    if align == "n":
        text_rect.midtop = (x, y)
    if align == "s":
        text_rect.midbottom = (x, y)
    if align == "e":
        text_rect.midright = (x, y)
    if align == "w":
        text_rect.midleft = (x, y)
    if align == "center":
        text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('playerShip1_orange.png').convert_alpha()
        self.image = pg.transform.rotate(self.image, -90)
        self.image_clean = self.image.copy()
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.rot_speed = 0
        self.rect.center = self.pos

    def get_keys(self):
        keys = pg.key.get_pressed()
        self.rot_speed = 0
        self.acc = vec(0, 0)
        if keys[pg.K_LEFT]:
            self.rot_speed = 90
        if keys[pg.K_RIGHT]:
            self.rot_speed = -90
        if keys[pg.K_UP]:
            self.acc = vec(250, 0)
        if keys[pg.K_DOWN]:
            self.acc = vec(-250, 0)

    def update(self, dt):
        self.get_keys()
        self.rot += self.rot_speed * dt
        self.rot = self.rot % 360
        self.image = pg.transform.rotate(self.image_clean, self.rot)
        self.rect = self.image.get_rect()
        self.acc = self.acc.rotate(-self.rot)
        self.vel += self.acc * dt
        self.pos += self.vel * dt + 0.5 * self.acc * dt**2
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        self.rect.center = self.pos

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
    all_sprites.update(dt)
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text("Rot: {:.2f}".format(player.rot), 18, WHITE, 10, 10, align="nw")
    pg.display.flip()

pg.quit()
