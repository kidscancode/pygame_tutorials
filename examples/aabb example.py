# AABB collision example
# KidsCanCode 2016

import pygame as pg
vec = pg.math.Vector2

WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0, 128)
GREEN = (0, 255, 0, 128)
CYAN = (0, 255, 255, 128)
YELLOW = (255, 255, 0)
LIGHTGRAY = (150, 150, 150)
DARKGRAY = (40, 40, 40)

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
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("AABB Collisions")

clock = pg.time.Clock()

p = pg.Rect(0, 0, 150, 150)
p.center = (WIDTH / 3, HEIGHT / 3)
m_r = pg.Rect(0, 0, 100, 100)
m = pg.Surface((100, 100)).convert_alpha()
col = GREEN
msg = ""

running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    m_r.center = (pg.mouse.get_pos())
    in_x = m_r.left < p.right and m_r.right > p.left
    in_y = m_r.top < p.bottom and m_r.bottom > p.top
    if in_x and in_y:
        # col = RED
        m.fill(RED)
        msg = "Colliding!"
    elif in_x or in_y:
        # col = CYAN
        m.fill(CYAN)
        msg = "Not colliding"
    else:
        # col = GREEN
        m.fill(GREEN)
        msg = "Not colliding"

    screen.fill(DARKGRAY)
    pg.draw.line(screen, LIGHTGRAY, (p.left, p.bottom + 5), (p.left, HEIGHT), 2)
    pg.draw.line(screen, LIGHTGRAY, (p.right, p.bottom + 5), (p.right, HEIGHT), 2)
    pg.draw.line(screen, LIGHTGRAY, (p.right + 5, p.top), (WIDTH, p.top), 2)
    pg.draw.line(screen, LIGHTGRAY, (p.right + 5, p.bottom), (WIDTH, p.bottom), 2)
    pg.draw.rect(screen, YELLOW, p)
    # pg.draw.rect(screen, col, m)
    screen.blit(m, m_r)
    draw_text(msg, 22, WHITE, 15, 15)
    draw_text("left", 18, WHITE, p.left - 5, HEIGHT - 5, align="se")
    draw_text("right", 18, WHITE, p.right + 5, HEIGHT - 5, align="sw")
    draw_text("top", 18, WHITE, WIDTH - 5, p.top - 5, align="se")
    draw_text("bottom", 18, WHITE, WIDTH - 5, p.bottom + 5, align="ne")
    draw_text(str(m_r), 20, col, WIDTH / 2, 15, align="nw")
    pg.display.flip()
