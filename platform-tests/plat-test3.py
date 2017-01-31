import pygame
from math import copysign

WIDTH = 800
HEIGHT = 640
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run!!!")
clock = pygame.time.Clock()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, vx, vy):
        super(Platform, self).__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        self.rect.x += self.vx
        # shift the player if we hit
        hits = pygame.sprite.collide_rect(self, player)
        if hits:
            if self.vx > 0:
                player.pos.x = self.rect.right
                player.rect.left = self.rect.right
            elif self.vx < 0:
                player.pos.x = self.rect.left - player.rect.width
                player.rect.right = self.rect.left

        self.rect.y += self.vy
        hits = pygame.sprite.collide_rect(self, player)
        if hits:
            if self.vy > 0:
                player.pos.y = self.rect.bottom
                player.rect.top = self.rect.bottom
            elif self.vy < 0:
                player.pos.y = self.rect.top - player.rect.height
                player.rect.bottom = self.rect.top

        if self.rect.right > WIDTH or self.rect.left < 0:
            self.vx *= -1
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.vy *= -1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.image = pygame.Surface([30, 30])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.friction = 0.18
        self.grav = 1

    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, walls, False)
        self.rect.y -= 2
        if hits:
            self.vel.y = -20

    def update(self):
        self.acc = pygame.math.Vector2(0, self.grav)
        a = 1.4
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.acc.x = -a
        if keystate[pygame.K_RIGHT]:
            self.acc.x = a

        # friction (x direction)
        self.acc.x += self.vel.x * -self.friction

        # moving platform below?
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, walls, False)
        self.rect.y -= 2
        if hits:
            if hits[0].vx != 0:
                self.pos.x += hits[0].vx
                self.rect.x = self.pos.x

        self.vel += self.acc
        # vertical movement first
        for y in range(1, abs(int(self.vel.y)) + 1):
            self.rect.y += copysign(1, self.vel.y)
            hits = pygame.sprite.spritecollide(self, walls, False)
            if hits:
                self.rect.y -= copysign(1, self.vel.y)
                self.vel.y = 0
                break
            else:
                self.pos.y += copysign(1, self.vel.y)

        # horiz. movement
        for x in range(1, abs(int(self.vel.x)) + 1):
            self.rect.x += copysign(1, self.vel.x)
            hits = pygame.sprite.spritecollide(self, walls, False)
            if hits:
                self.rect.x -= copysign(1, self.vel.x)
                self.vel.x = 0
                break
            else:
                self.pos.x += copysign(1, self.vel.x)

        if self.pos.x < 0:
            self.pos.x = 0
            self.rect.x = 0
        if self.pos.x > WIDTH - self.rect.width:
            self.pos.x = WIDTH - self.rect.width
            self.rect.right = WIDTH

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
walls = pygame.sprite.Group()
p_list = [[0, HEIGHT - 32, WIDTH, 32, 0, 0],
          [100, HEIGHT - 160, 250, 32, 0, 0],
          [200, HEIGHT - 288, 200, 32, 0, 0],
          [0, HEIGHT - 320, 100, 32, 2, 0],
          [0, 150, 110, 32, -3, 0],
          [WIDTH - 100, 0, 100, 32, 0, 2]]
for loc in p_list:
    plat = Platform(loc[0], loc[1], loc[2], loc[3], loc[4], loc[5])
    all_sprites.add(plat)
    walls.add(plat)

# GAME LOOP
running = True
while running:
    clock.tick(FPS)
    # Check for events
    for event in pygame.event.get():
        # close the window
        if event.type == pygame.QUIT:
            running = False
        # check for key presses
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                player.jump()

    # all_sprites.update()
    walls.update()
    player.update()
    # DRAW THE SCREEN
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
