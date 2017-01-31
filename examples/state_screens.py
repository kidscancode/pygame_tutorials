import pygame as pg

WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BGCOLOR = (40, 40, 40)

font_name = pg.font.match_font('hack')
def draw_text(surf, text, size, color, x, y, align="topleft"):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    surf.blit(text_surface, text_rect)

class Scene:
    def __init__(self):
        self.next = self
        self.name = type(self).__name__

    def process_input(self, events):
        for event in events:
            if event.type == pg.KEYDOWN and event.key in scenes[self.name]:
                self.switch_to(scenes[self.name][event.key]())

    def update(self):
        pass

    def draw(self, screen):
        pass

    def switch_to(self, next_scene):
        self.next = next_scene

    def end(self):
        self.next = None

class TitleScreen(Scene):
    def __init__(self):
        Scene.__init__(self)

    def draw(self, screen):
        screen.fill(BGCOLOR)
        draw_text(screen, "GET READY", 50, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        draw_text(screen, "press <space> to start", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        draw_text(screen, "press <m> for menu", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4 + 50, align="center")

class GameScreen(Scene):
    def __init__(self):
        Scene.__init__(self)

    def draw(self, screen):
        screen.fill(BGCOLOR)
        draw_text(screen, "YOU'RE PLAYING", 50, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        draw_text(screen, "press <q> to end", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")

class MenuScreen(Scene):
    def __init__(self):
        Scene.__init__(self)

    def draw(self, screen):
        screen.fill(BGCOLOR)
        draw_text(screen, "SETTINGS", 50, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        draw_text(screen, "press <ESC> to return", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")

class EndScreen(Scene):
    def __init__(self):
        Scene.__init__(self)

    def draw(self, screen):
        screen.fill(BGCOLOR)
        draw_text(screen, "GAME OVER", 50, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        draw_text(screen, "press <r> to restart", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")

scenes = {'TitleScreen': {pg.K_SPACE: GameScreen,
                          pg.K_m: MenuScreen},
          'MenuScreen': {pg.K_ESCAPE: TitleScreen},
          'GameScreen': {pg.K_q: EndScreen},
          'EndScreen': {pg.K_r: TitleScreen}}

def main(start_scene):
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    scene = start_scene

    while scene:
        pg.display.set_caption(scene.name)
        clock.tick(FPS)
        events = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                scene.end()
            else:
                events.append(event)

        scene.process_input(events)
        scene.update()
        scene.draw(screen)
        pg.display.flip()

        scene = scene.next

main(TitleScreen())
