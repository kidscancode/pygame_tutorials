# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

WIDTH = 360
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image0 = img
        self.image0.set_colorkey(BLACK)
        self.image = self.image0.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speedx = 0
        self.rot = 0
        self.rot_speed = 5
        self.last_update = pygame.time.get_ticks()

    def update(self):
        if not good_rotation:
            self.update_bad()
        else:
            self.update_good()

    def update_bad(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image0, self.rot)

    def update_good(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image0, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

img = pygame.image.load(path.join(path.dirname(__file__), "playerShip1_orange.png")).convert()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

print("p: pause")
print("r: draw original rect")
print("f: draw fixed rect")
print("<space>: rotate corner/center")
# Game loop
good_rotation = False
draw_orig_rect = False
draw_fixed_rect = False
pause = True
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                draw_orig_rect = not draw_orig_rect
            if event.key == pygame.K_p:
                pause = not pause
            if event.key == pygame.K_f:
                draw_fixed_rect = not draw_fixed_rect
            if event.key == pygame.K_SPACE:
                good_rotation = not good_rotation
                player.kill()
                player = Player()
                all_sprites.add(player)

    # Update
    if not pause:
        all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    if draw_orig_rect:
        pygame.draw.rect(screen, WHITE, player.rect, 5)
    p_rect = player.image.get_rect()
    p_rect.topleft = player.rect.topleft
    if draw_fixed_rect:
        pygame.draw.rect(screen, WHITE, p_rect, 2)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
