from game import Game
from config import *

if __name__ == "__main__":
    s = Game(
        bg_path = 'resources/background.jpg',
        music_path = 'resources/bg_music_1.mp3',
        body_path = 'resources/block.jpg',
        apple_path = 'resources/apple.jpg',
        width = SCREEN_WIDTH,
        height = SCREEN_HEIGHT,
        length = LENGTH
    )
    s.run()