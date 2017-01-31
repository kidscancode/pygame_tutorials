# game options/settings
TITLE = "Jumpy!"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
