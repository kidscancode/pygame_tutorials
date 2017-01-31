import pygame as pg
import random as rand

WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Platformer"

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)

class Plat(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.game = game
        self.vx = 0
        self.vy = 0
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 350

    def jump_cut(self):
        if self.vy < -3:
            self.vy = -3

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.plats, False)
        self.rect.y -= 2
        if hits:
            self.vy = -20

    def update(self):
        self.vx = 0
        self.vy += 1  # GRAVITY
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.vx = -5
        if keystate[pg.K_RIGHT]:
            self.vx = 5
        self.rect.x += self.vx
        self.rect.y += self.vy

class Game:
    # Game object contains all pieces of the game

    def __init__(self):
        # initialize first time, create window
        pg.init()
        # sound
        pg.mixer.init()
        # create the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # create clock for FPS timing
        self.clock = pg.time.Clock()

    def new(self):
        # start a new game (reset)
        self.all_sprites = pg.sprite.Group()
        self.plats = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        plat = Plat(0, HEIGHT - 40, WIDTH, 40)
        self.all_sprites.add(plat)
        self.plats.add(plat)

    def run(self):
        # run the game loop
        self.running = True
        self.new()
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Handle events or input
        for event in pg.event.get():
            # close the window when x clicked
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def update(self):
        # Update the game state
        self.all_sprites.update()
        # collide player with platforms
        hits = pg.sprite.spritecollide(self.player, self.plats, False)
        if hits:
            self.player.vy = 0
            self.player.rect.bottom = hits[0].rect.top

    def draw(self):
        # draw the next frame
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        # show the start screen/menu/etc
        pass

    def show_game_over_screen(self):
        # you lost
        pass

game = Game()
while True:
    game.show_start_screen()
    game.run()
    game.show_game_over_screen()
