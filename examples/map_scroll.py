# visual aid for map scrolling tutorial
import pygame as pg

WIDTH = 800
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Scrolling Map")
clock = pg.time.Clock()
vec = pg.math.Vector2
pg.key.set_repeat(500, 100)

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

GAME_SCREEN_W = 256
GAME_SCREEN_H = 192
game_screen = pg.Rect(WIDTH / 2 - GAME_SCREEN_W / 2 - 100, HEIGHT / 2 - GAME_SCREEN_H / 2 - 50, 256, 192)
map_rect = pg.Rect(game_screen.x, game_screen.y, 512, 384)
player_rect = pg.Rect(game_screen.x + GAME_SCREEN_W / 2, game_screen.y + GAME_SCREEN_H / 2, 8, 8)

offset = vec(0, 0)
player_pos = vec(16, 12)
# Game loop
running = True
while running:
    # keep loop running at the right speed
    dt = clock.tick(FPS) / 1000
    # Process input (events)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                map_rect.x -= 8
                offset.x -= 1
                player_pos.x += 1
            if event.key == pg.K_LEFT:
                map_rect.x += 8
                offset.x += 1
                player_pos.x -= 1
            if event.key == pg.K_UP:
                map_rect.y += 8
                offset.y += 1
                player_pos.y -= 1
            if event.key == pg.K_DOWN:
                map_rect.y -= 8
                offset.y -= 1
                player_pos.y += 1

    # Update

    # Draw / render
    screen.fill(BLACK)
    pg.draw.rect(screen, GREEN, map_rect, 4)
    pg.draw.rect(screen, RED, game_screen, 4)
    pg.draw.rect(screen, YELLOW, player_rect)
    draw_text("draw offset:", 22, WHITE, 10, 10)
    draw_text(str(offset), 22, WHITE, 10, 40)
    draw_text("player.pos:", 22, WHITE, WIDTH - 10, 10, align="ne")
    draw_text(str(player_pos), 22, WHITE, WIDTH - 10, 40, align="ne")
    draw_text("screen: (1024, 768)", 18, RED, game_screen.left + 5, game_screen.bottom + 5)
    draw_text("map: (2048, 1536)", 18, GREEN, map_rect.left + 5, map_rect.bottom + 5)
    # pg.draw.line(screen, WHITE, player.pos, pg.mouse.get_pos(), 2)
    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()
