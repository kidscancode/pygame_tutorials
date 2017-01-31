# player sprite, simple map (map example?)
# shake when space is pressed
# way to adjust amount/times
import pygame as pg
from itertools import repeat

WIDTH = 800
HEIGHT = 640
TILE_SIZE = 32
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
GREY = (40, 40, 40)

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
game_surface = pg.Surface((WIDTH, HEIGHT))
pg.display.set_caption("Screen Shake Demo")
clock = pg.time.Clock()

def shake(amount=10, step=4, times=2):
    # implement screen shake
    direction = -1
    for _ in range(0, times):
        for x in range(0, amount, step):
            yield(x * direction, x * direction)
        for x in range(amount, 0, -step):
            yield(x * direction, x * direction)
        direction *= -1
    while True:
        yield (0, 0)

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y):
        groups = all_sprites, walls
        pg.sprite.Sprite.__init__(self, groups)
        self.image = pg.Surface((32, 32))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -300
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = 300
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -300
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = 300
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

all_sprites = pg.sprite.Group()
walls = pg.sprite.Group()
offset = repeat((0, 0))
# load map file
map_data = []
with open('map.txt', 'rt') as f:
    for line in f:
        map_data.append(line)
for row, tiles in enumerate(map_data):
    for col, tile in enumerate(tiles):
        if tile == '1':
            Wall(col, row)
        if tile == 'P':
            p = Player(col, row)
# Game loop
running = True
while running:
    dt = clock.tick(FPS) / 1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                offset = shake(amount=5, step=2, times=2)

    all_sprites.update()

    game_surface.fill(BLACK)
    all_sprites.draw(game_surface)
    screen.blit(game_surface, next(offset))
    pg.display.flip()

pg.quit()
