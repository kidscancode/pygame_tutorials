import pygame as pg
from itertools import cycle
import pytweening as tween

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTGREY = (40, 40, 40)

tween_func = cycle([tween.easeInSine, tween.easeOutSine, tween.easeInOutSine,
                    tween.easeInCirc, tween.easeOutCirc, tween.easeInOutCirc,
                    tween.easeInQuart, tween.easeOutQuart, tween.easeInOutQuart,
                    tween.easeInQuint, tween.easeOutQuint, tween.easeInOutQuint,
                    tween.easeInExpo, tween.easeOutExpo, tween.easeInOutExpo,
                    tween.easeInElastic, tween.easeOutElastic, tween.easeInOutElastic,
                    tween.easeInBounce, tween.easeOutBounce, tween.easeInOutBounce])

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

pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

class Box(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.iter = 0

    def update(self, dt):
        self.rect.x = 750 * tween.linear(self.iter / ITERATIONS)
        self.rect.y = 10 + 550 * func(self.iter / ITERATIONS)
        self.iter += 1
        if self.iter > ITERATIONS:
            self.iter = 0

ITERATIONS = 400
factor = 0
func = next(tween_func)
draw_text("Func: {}".format(func.__name__), 22, WHITE, 795, 5, align="ne")
b = Box()

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                func = next(tween_func)
                screen.fill((0, 0, 0))
                draw_text("Func: {}".format(func.__name__), 22, WHITE, 795, 5, align="ne")
                b = Box()

    b.update(dt)

    # screen.fill((0, 0, 0))
    screen.blit(b.image, b.rect)
    pg.display.flip()

pg.quit()
