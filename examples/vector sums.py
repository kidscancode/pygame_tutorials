
import pygame
import random

WIDTH = 1000
HEIGHT = 800
FPS = 30

NUM_MOBS = 3
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Motion Demo")
clock = pygame.time.Clock()
vec = pygame.math.Vector2

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type, col):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(col)
        self.type = type
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos


def draw_text(text, size, col, x, y):
    # utility function to draw text on screen
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, col)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_all():
    for mob in mobs:
        a = (player.pos - mob.pos).normalize() * 200
        draw_arrow(mob.pos, (mob.pos + a), CYAN, 5)
        tot = vec(0, 0)
        for other in mobs:
            if other != mob:
                dv = (mob.pos - other.pos)
                dv = dv * 10000 / dv.length_squared()
                tot += dv
                draw_arrow(mob.pos, (mob.pos + dv), RED, 1)
        draw_arrow(mob.pos, (mob.pos + tot), RED, 5)
        a_tot = a + tot
        draw_arrow(mob.pos, (mob.pos + a_tot), GREEN, 8)

def draw_arrow(p1, p2, col, size):
    # line portion
    pygame.draw.line(screen, col, p1, p2, size)
    # triangle portion
    # if p2.x > p1.x:
    #     t1 = (p2.x + 5, p2.y)
    #     t2 = (p2.x-10, p2.y+10)
    #     t3 = (p2.x-10, p2.y-10)
    # else:
    #     t1 = (p2.x - 5, p2.y)
    #     t2 = (p2.x+10, p2.y+10)
    #     t3 = (p2.x+10, p2.y-10)
    # pygame.draw.polygon(screen, col, [t1, t2, t3])

def spawn_mobs():
    for mob in mobs:
        mob.kill()
    for i in range(NUM_MOBS):
        i = Item(random.randrange(WIDTH), random.randrange(HEIGHT), 'mob', RED)
        all_sprites.add(i)
        mobs.add(i)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Item(WIDTH / 2, HEIGHT / 2, 'player', CYAN)
all_sprites.add(player)
spawn_mobs()

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            spawn_mobs()

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_all()
    # txt = "Acc: ({:.2f}, {:.2f})".format(player.acc.x, player.acc.y)
    # draw_text(txt, 25, RED, 5, 105)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
