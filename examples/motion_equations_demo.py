# Motion Demo - demonstrate equations of motion
# This is a simple demo to illustrate the effects of
# using the equations of motion - acceleration, velocity,
# and position - for movement of a sprite.
import pygame
import random

WIDTH = 1000
HEIGHT = 800
FPS = 30

PLAYER_ACC = 0.7
PLAYER_REACT = 1
PLAYER_MAX_VEL = 30
FRICTION = -0.08

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Motion Demo")
clock = pygame.time.Clock()
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 80))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pygame.K_UP]:
            self.acc.y = -PLAYER_ACC
        if keys[pygame.K_DOWN]:
            self.acc.y = PLAYER_ACC
        if keys[pygame.K_SPACE]:
            self.acc = vec(0, 0)
            self.vel = vec(0, 0)

        # check if acc dir is opposite vel dir
        # if so, boost accel a little bit
        if (self.vel.x < 0) == (self.acc.x < 0):
            self.acc = self.acc
        else:
            self.acc = self.acc + self.acc * PLAYER_REACT

        # friction
        #self.acc += self.vel * FRICTION

        # minimum val
        if self.vel.length_squared() < 0.1:
            self.vel = vec(0, 0)

        self.vel += self.acc
        # terminal vel
        if self.vel.length_squared() > PLAYER_MAX_VEL ** 2:
            self.vel = self.vel.normalize() * PLAYER_MAX_VEL
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.center = self.pos

def draw_text(text, size, col, x, y):
    # utility function to draw text on screen
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, col)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_vectors(obj):
    # velocity
    # if obj.vel.x != 0:
    draw_arrow(obj.pos, (obj.pos + obj.vel * 20), GREEN, 7)
    # accel
    # if obj.acc.x != 0:
    draw_arrow(obj.pos, (obj.pos + obj.acc * 400), RED, 3)

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

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
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

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_vectors(player)
    txt = "Pos: ({:.2f}, {:.2f})".format(player.pos.x, player.pos.y)
    draw_text(txt, 25, WHITE, 5, 5)
    txt = "Vel: ({:.2f}, {:.2f})".format(player.vel.x, player.vel.y)
    draw_text(txt, 25, GREEN, 5, 55)
    txt = "Acc: ({:.2f}, {:.2f})".format(player.acc.x, player.acc.y)
    draw_text(txt, 25, RED, 5, 105)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
