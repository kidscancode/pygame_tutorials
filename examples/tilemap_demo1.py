# demo1 - simple grid-based movement (4 directional), tile-based collisions
import pygame as pg

WIDTH = 800
HEIGHT = 640
TILE_SIZE = 32
TILE_WIDTH = WIDTH / TILE_SIZE
TILE_HEIGHT = HEIGHT / TILE_SIZE
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

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y):
        groups = all_sprites, walls
        pg.sprite.Sprite.__init__(self, groups)
        self.image = pg.Surface((32, 32))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        groups = all_sprites
        pg.sprite.Sprite.__init__(self, groups)
        self.image = pg.Surface((32, 32))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def collide_walls(self):
        for wall in walls:
            if wall.x == self.x and wall.y == self.y:
                return True
        return False

    def move(self, dx=0, dy=0):
        self.x += dx
        if self.collide_walls():
            self.x -= dx
        self.y += dy
        if self.collide_walls():
            self.y -= dy
        if self.x == -1:
            self.x = TILE_WIDTH - 1
        if self.x == TILE_WIDTH:
            self.x = 0
        if self.y == -1:
            self.y = TILE_HEIGHT - 1
        if self.y == TILE_HEIGHT:
            self.y = 0

    def update(self):
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

all_sprites = pg.sprite.Group()
walls = pg.sprite.Group()
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
pg.key.set_repeat(500, 100)
# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_LEFT:
                p.move(dx=-1, dy=0)
            if event.key == pg.K_RIGHT:
                p.move(dx=1, dy=0)
            if event.key == pg.K_UP:
                p.move(dx=0, dy=-1)
            if event.key == pg.K_DOWN:
                p.move(dx=0, dy=1)

    # Update
    all_sprites.update()

    screen.fill((40, 40, 40))
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()
