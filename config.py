START_POS = (120, 120)
BODY_SIZE = (40, 40)
APPLE_SIZE = (40, 40)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 680
SCORE_POS = (SCREEN_WIDTH - 150, 10)
N_WIDTH = SCREEN_WIDTH // BODY_SIZE[0]
N_HEIGHT = SCREEN_HEIGHT // BODY_SIZE[0]
LENGTH = 1
BG_POSITION = (0, 0)
FONT_NAME = 'arial'
FONT_SIZE = 20
SCORE_COLOR = (255, 255, 255)
OVER_SIZE = 50
OVER_POS = (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)
OVER_COLOR = (255, 0, 0)
OVER_SCREEN_COLOR = (0, 0, 0)
TITLE = 'Snake'
APPLE_START_POS = (400, 400)

class Direction:
    def __init__(self):
        self.direction = {
            0 : "RIGHT",
            1 : "LEFT",
            2 : "UP",
            3 : "DOWN"
        }