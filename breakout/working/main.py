# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 2
# Video link: https://www.youtube.com/watch?v=8LRI0RLKyt0
# Player movement

import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font('arial')

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.bricks = pg.sprite.Group()
        self.create_bricks()
        self.paddle = Paddle()
        self.all_sprites.add(self.paddle)
        self.ball = Ball()
        self.all_sprites.add(self.ball)
        self.run()

    def create_bricks(self):
        # Create a grid of bricks (14 x 5)
        padding = (WIDTH - (BRICK_WIDTH + BRICK_SPACING) * BRICK_COLS) // 2
        for y in range(BRICK_ROWS):
            for x in range(BRICK_COLS):
                brick = Brick(padding + x * (BRICK_WIDTH + BRICK_SPACING),
                              BRICK_HEIGHT * 2 + y * (BRICK_HEIGHT + BRICK_SPACING),
                              BRICK_COLORS[y])
                self.all_sprites.add(brick)
                self.bricks.add(brick)

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

    def draw_text(surf, text, size, x, y):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
