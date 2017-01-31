# pg template - skeleton for a new pg project
import pygame as pg
from random import randint, uniform
vec = pg.math.Vector2

WIDTH = 1024
HEIGHT = 800
FPS = 60
GRIDSIZE = 32
NUM_MOBS = 1
MOB_SIZE = 16
NEIGHBOR_RADIUS = 75
ALIGN_WEIGHT = 1
COHERE_WEIGHT = 1.2
SEPARATE_WEIGHT = 1.6
MAX_SPEED = 5
MAX_FORCE = 0.2
APPROACH_RADIUS = 100
SEEK_RADIUS = 300

WANDER_RADIUS = 150
WANDER_DISTANCE = 255
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
LIGHTGREY = (40, 40, 40)

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flocking Example")
clock = pg.time.Clock()

def draw_text(text, size, color, x, y, align="topleft"):
    font_name = pg.font.match_font('hack')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    screen.blit(text_surface, text_rect)

def draw_grid():
    for x in range(0, WIDTH, GRIDSIZE):
        pg.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRIDSIZE):
        pg.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.rect.center = self.pos

    def update(self):
        self.vel = vec(0, 0)
        self.move_8way()
        self.pos += self.vel
        self.rect.center = self.pos
        # prevent sprite from moving off screen
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        if self.pos.y > HEIGHT:
            self.pos.y = 0

    def move_8way(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            self.vel.y = -5
        if keystate[pg.K_DOWN]:
            self.vel.y = 5
        if keystate[pg.K_LEFT]:
            self.vel.x = -5
        if keystate[pg.K_RIGHT]:
            self.vel.x = 5

class Predator(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites, predators
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((16, 16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(25, WIDTH - 25), randint(25, HEIGHT - 25))
        self.vel = vec(3, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos

    def wander(self):
        steer = vec(0, 0)
        future = self.pos + self.vel.normalize() * WANDER_DISTANCE
        target = future + vec(WANDER_RADIUS, 0).rotate(uniform(0, 360))
        steer = self.seek(target)
        self.draw_data = [future, target]
        return steer

    def seek(self, target):
        desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (desired - self.vel)
        if steer.length_squared() > 0.2**2:
            steer.scale_to_length(0.2)
        return steer

    def update(self):
        wander = self.wander()
        seek = vec(0, 0)

        self.acc = seek + wander
        self.vel += self.acc
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.center = self.pos

class Mob(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites, mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((MOB_SIZE, MOB_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(25, WIDTH - 25), randint(25, HEIGHT - 25))
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos

    def seek(self, target):
        steer = vec(0, 0)
        dist = target - self.pos
        if dist.length_squared() < SEEK_RADIUS**2:
            desired = dist.normalize() * MAX_SPEED
            steer = desired - self.vel
            if steer.length_squared() > MAX_FORCE**2:
                steer.scale_to_length(MAX_FORCE)
        return steer

    def separation(self, a_dist):
        # move away from other mobs
        desired = a_dist
        if desired.length_squared() > 0:
            desired.scale_to_length(MAX_SPEED)
        steer = (desired - self.vel)
        if steer.length_squared() > MAX_FORCE**2:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def alignment(self, a_vel):
        desired = a_vel
        desired.scale_to_length(MAX_SPEED)
        steer = (desired - self.vel)
        if steer.length_squared() > MAX_FORCE**2:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def cohesion(self, a_pos):
        desired = a_pos
        steer = self.seek(desired)
        return steer

    def get_averages(self):
        count = 0
        a_pos = vec(0, 0)
        a_dist = vec(0, 0)
        a_vel = vec(0, 0)
        for mob in mobs:
            if mob != self:
                d = self.pos.distance_to(mob.pos)
                if d < NEIGHBOR_RADIUS:
                    a_pos += mob.pos
                    a_vel += mob.vel
                    a_dist += (self.pos - mob.pos).normalize() / d
                    count += 1
        if count > 0:
            a_pos /= count
            a_vel /= count
            a_dist /= count
        return count, a_pos, a_dist, a_vel

    def update(self):
        # avoid multiple loops, get averages
        count, a_pos, a_dist, a_vel = self.get_averages()
        # self.acc = self.seek(pg.mouse.get_pos())
        # self.acc = vec(0, 0)
        if count > 0:
            sep = self.separation(a_dist) * SEPARATE_WEIGHT
            ali = self.alignment(a_vel) * ALIGN_WEIGHT
            coh = self.cohesion(a_pos) * COHERE_WEIGHT
            self.acc += sep + ali + coh
        if self.acc.length_squared() == 0 and self.vel.length() < MAX_SPEED:
            desired = self.vel.normalize() * MAX_SPEED
            self.acc = desired - self.vel
        self.acc += self.seek(p1.pos) * 0.75
        if self.acc.length_squared() > MAX_FORCE**2:
            self.acc.scale_to_length(MAX_FORCE)
        self.vel += self.acc
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.center = self.pos

    def draw_vectors(self):
        scale = 10
        # vel
        pg.draw.line(screen, GREEN, self.pos, (self.pos + self.vel * scale), 5)
        # acc
        pg.draw.line(screen, RED, self.pos, (self.pos + self.acc * scale * 5), 5)
        # rad
        pg.draw.circle(screen, CYAN, (int(self.pos.x), int(self.pos.y)), NEIGHBOR_RADIUS, 1)

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
predators = pg.sprite.Group()
# p1 = Predator()
p1 = Player()
all_sprites.add(p1)
for i in range(NUM_MOBS):
    Mob()
paused = False
show_vectors = False

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
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                paused = not paused
            if event.key == pg.K_m:
                Mob()
            if event.key == pg.K_v:
                show_vectors = not show_vectors
            if event.key == pg.K_q:
                ALIGN_WEIGHT += 0.1
            if event.key == pg.K_z:
                ALIGN_WEIGHT -= 0.1
            if event.key == pg.K_w:
                SEPARATE_WEIGHT += 0.1
            if event.key == pg.K_x:
                SEPARATE_WEIGHT -= 0.1
            if event.key == pg.K_e:
                COHERE_WEIGHT += 0.1
            if event.key == pg.K_c:
                COHERE_WEIGHT -= 0.1
            if event.key == pg.K_t:
                NEIGHBOR_RADIUS += 5
            if event.key == pg.K_b:
                NEIGHBOR_RADIUS -= 5

    # Update
    p1.update()
    if not paused:
        mobs.update()
        predators.update()

    # Draw / render
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(BLACK)
    draw_grid()
    all_sprites.draw(screen)
    draw_text("A: {:.1f}".format(ALIGN_WEIGHT), 18, WHITE, 5, 5)
    draw_text("S: {:.1f}".format(SEPARATE_WEIGHT), 18, WHITE, 5, 25)
    draw_text("C: {:.1f}".format(COHERE_WEIGHT), 18, WHITE, 5, 45)
    draw_text("R: {}".format(NEIGHBOR_RADIUS), 18, WHITE, 5, 65)
    if show_vectors:
        for sprite in mobs:
            sprite.draw_vectors()
    pg.display.flip()

pg.quit()
