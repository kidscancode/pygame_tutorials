# pg template - skeleton for a new pg project
import pygame as pg
from random import randint
vec = pg.math.Vector2

WIDTH = 1024
HEIGHT = 800
FPS = 100
TILESIZE = 20
GRIDSIZE = 32
MOB_SIZE = 10
NUM_MOBS = 1000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTGREY = (40, 40, 40)

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Spatial Hash Example")
clock = pg.time.Clock()

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

def draw_grid():
    for x in range(0, WIDTH, GRIDSIZE):
        pg.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRIDSIZE):
        pg.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))

def rect_quad_split(rect):
    # split a given rect into 4 equal parts
    w = rect.width / 2
    h = rect.height / 2
    rects = []
    rects.append(pg.Rect(rect.left, rect.top, w, h))
    rects.append(pg.Rect(rect.left + w, rect.top, w, h))
    rects.append(pg.Rect(rect.left, rect.top + h, w, h))
    rects.append(pg.Rect(rect.left + w, rect.top + h, w, h))
    return rects

class QuadTree:
    def __init__(self, level, rect, items=[]):
        self.maxlevel = 4
        self.level = level
        self.maxitems = 4
        self.rect = rect
        self.items = items
        self.branches = []

    def subdivide(self):
        for rect in rect_quad_split(self.rect):
            branch = QuadTree(self.level + 1, rect, [])
            self.branches.append(branch)

    def add_item(self, item):
        self.items.append(item)

    def subdivide_items(self):
        for item in self.items:
            for branch in self.branches:
                if branch.rect.colliderect(item.rect):
                    branch.add_item(item)

    def possible_collisions(self, rect):
        items = []
        for branch in self.branches:
            if rect.colliderect(branch.rect):
                items += branch.items

    def render(self, surf):
        col = [int(255 / self.level) for i in range(3)]
        pg.draw.rect(surf, col, self.rect)

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.vx, self.vy = 0, 0
        self.move_8way()
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

    def move_8way(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            self.vy = -5
        if keystate[pg.K_DOWN]:
            self.vy = 5
        if keystate[pg.K_LEFT]:
            self.vx = -5
        if keystate[pg.K_RIGHT]:
            self.vx = 5
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

class Mob(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites, mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((MOB_SIZE, MOB_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(0, WIDTH), randint(0, HEIGHT))
        self.rect.center = self.pos
        self.vel = vec(2, 0).rotate(randint(0, 360))

    def update(self):
        if use_hash:
            game_hash.remove_item(self)
        self.pos += self.vel
        if self.pos.x > WIDTH or self.pos.x < 0:
            self.vel.x *= -1
        if self.pos.y < 0 or self.pos.y > HEIGHT:
            self.vel.y *= -1
        self.rect.center = self.pos
        if use_hash:
            game_hash.add_item(self)

all_sprites = pg.sprite.Group()
game_hash = SpatialHash(cellsize=TILESIZE)
mobs = pg.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(NUM_MOBS):
    game_hash.add_item(Mob())
draw_hash = False
use_hash = True
paused = False

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
        if event.type == pg.KEYDOWN and event.key == pg.K_h:
            draw_hash = not draw_hash
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            paused = not paused
        if event.type == pg.KEYDOWN and event.key == pg.K_c:
            use_hash = not use_hash

    # Update
    player.update()
    if not paused:
        mobs.update()
    if use_hash:
        nearby_mobs = pg.sprite.Group()
        nearby_mobs.add(game_hash.pot_coll(player.rect.inflate(30, 30)))
        hits = pg.sprite.spritecollide(player, nearby_mobs, False)
        for hit in hits:
            hit.kill()
    else:
        hits = pg.sprite.spritecollide(player, mobs, False)
        for hit in hits:
            hit.kill()

    # Draw / render
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(BLACK)
    draw_grid()
    all_sprites.draw(screen)
    draw_text("use_hash:{}".format(use_hash), 18, WHITE, 5, 5, align="nw")
    draw_text("mobs: {}".format(len(mobs)), 18, WHITE, 5, 22, align="nw")
    if draw_hash:
        for cell in game_hash.d.keys():
            p_rect = player.rect.inflate(30, 30)
            r = pg.Rect(cell[0] * TILESIZE, cell[1] * TILESIZE, TILESIZE, TILESIZE)
            pg.draw.rect(screen, YELLOW, r, 2)
            pg.draw.rect(screen, WHITE, p_rect, 1)
            p_collide = game_hash.cells_for_rect2(p_rect)
            for c in p_collide:
                if c in game_hash.d:
                    r = pg.Rect(c[0] * TILESIZE, c[1] * TILESIZE, TILESIZE, TILESIZE)
                    pg.draw.rect(screen, RED, r, 2)
    pg.display.flip()

pg.quit()
