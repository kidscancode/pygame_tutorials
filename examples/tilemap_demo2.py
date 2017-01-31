# demo2 -
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
GREY = (40, 40, 40)

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

def draw_grid():
    for x in range(0, WIDTH, TILE_SIZE):
        pg.draw.line(screen, GREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE):
        pg.draw.line(screen, GREY, (0, y), (WIDTH, y))

class Wall(pg.sprite.Sprite):
    def __init__(self):
        groups = all_sprites, walls
        pg.sprite.Sprite.__init__(self, groups)
        self.image = pg.Surface((640, 320))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        pg.draw.polygon(self.image, MAGENTA, [(640, 160), (640, 320), (0, 320)])
        self.mask = pg.mask.from_surface(self.image)
        self.rect.right = WIDTH - 64
        self.rect.bottom = HEIGHT - 64

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        groups = all_sprites
        pg.sprite.Sprite.__init__(self, groups)
        self.image = pg.Surface((32, 32))
        self.image.fill(YELLOW)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.x = x
        self.y = y

    def update(self):
        pg.display.set_caption(str((self.rect.x, self.rect.y)))
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.vy = -5
        if keys[pg.K_DOWN]:
            self.vy = 5
        if keys[pg.K_LEFT]:
            self.vx = -5
        if keys[pg.K_RIGHT]:
            self.vx = 5
        # if self.vx != 0 and self.vy != 0:
        #     self.vx *= 0.7071
        #     self.vy *= 0.7071
        self.rect.x += self.vx
        if pg.sprite.spritecollide(self, walls, False, pg.sprite.collide_mask):
            self.rect.x -= self.vx
        self.rect.y += self.vy
        if pg.sprite.spritecollide(self, walls, False, pg.sprite.collide_mask):
            self.rect.y -= self.vy

all_sprites = pg.sprite.Group()
walls = pg.sprite.Group()
p = Player(12, 10)
w = Wall()
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

    all_sprites.update()

    screen.fill(BLACK)
    draw_grid()
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()
