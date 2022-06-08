import numpy as np
from config import *
import pygame
from snake import Snake

class Apple:
    def __init__(self, snake : Snake):
        self.apple_Position = (APPLE_SIZE[0] * np.random.randint(N_WIDTH), APPLE_SIZE[1] * np.random.randint(N_HEIGHT))

    def _appleInSnake(self, x : int ,y : int, snake : Snake):
        for i in range(snake.length):
            position = snake.body_Positions[i]
            if position == (x, y) : return True
        return False

    def _getCoords(self, snake : Snake):
        x = APPLE_SIZE[0] * np.random.randint(N_WIDTH)
        y = APPLE_SIZE[1] * np.random.randint(N_HEIGHT)
        while self._appleInSnake(x, y, snake):
            x = APPLE_SIZE[0] * np.random.randint(N_WIDTH)
            y = APPLE_SIZE[1] * np.random.randint(N_HEIGHT)
        return (x, y)
