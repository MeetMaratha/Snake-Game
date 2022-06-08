import pygame
import numpy as np
from config import *
from AI import Game


if __name__ == "__main__":
    game = Game(
        width = SCREEN_WIDTH,
        height = SCREEN_HEIGHT,
        bg_Path = '../resources/background.jpg',
        apple_Path = '../resources/apple.jpg',
        body_Path = '../resources/block.jpg',
        ding_Path = '../resources/ding.mp3',
        crash_Path = '../resources/crash.mp3',
        title = TITLE
    )
    game.run('../resources/bg_music_1.mp3')