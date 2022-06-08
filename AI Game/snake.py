import numpy as np
from config import *
import pygame

class Snake:
    def __init__(self, position : tuple, length : int):

        self.head_Position = position
        self.length = length
        self.direction_Dict = Direction().direction
        self.body_Positions = [(START_POS[0], START_POS[1] - BODY_SIZE[1] * i) for i in range(self.length)]
        self.direction = self.direction_Dict[3]
        self.body_Direction = [self.direction_Dict[3]] * self.length

    def _setDirection(self, action):
        self.direction = self.direction_Dict[action]
    
    def move(self):
        for i in range(self.length - 1, 0, -1):
            self.body_Positions[i] = self.body_Positions[i - 1]
            self.body_Direction[i] = self.body_Direction[i - 1]
        if self.direction == self.direction_Dict[0]:
            self.body_Positions[0] = (
                self.body_Positions[0][0] + BODY_SIZE[0],
                self.body_Positions[0][1]
                )
        elif self.direction == self.direction_Dict[1]:
            self.body_Positions[0] = (
                self.body_Positions[0][0] - BODY_SIZE[0], 
                self.body_Positions[0][1]
                )
        elif self.direction == self.direction_Dict[2]:
            self.body_Positions[0] = (
                self.body_Positions[0][0],
                self.body_Positions[0][1] - BODY_SIZE[1]
                )
        elif self.direction == self.direction_Dict[3]:
            self.body_Positions[0] = (
                self.body_Positions[0][0], 
                self.body_Positions[0][1] + BODY_SIZE[1]
                )
        self.head_Position = self.body_Positions[0]
        self.body_Direction[0] = self.direction
        
    def _getNewCoords(self):
        if self.direction == self.direction_Dict[0]:
            x = self.head_Position[0] + BODY_SIZE[0]
            y = self.head_Position[1]
        elif self.direction == self.direction_Dict[1]:
            x = self.head_Position[0] - BODY_SIZE[0]
            y = self.head_Position[1]
        elif self.direction == self.direction_Dict[2]:
            x = self.head_Position[0]
            y = self.head_Position[1] - BODY_SIZE[1]
        elif self.direction == self.direction_Dict[3]:
            x = self.head_Position[0]
            y = self.head_Position[1] + BODY_SIZE[1]
        return x, y
    
    def _increaseSnake(self):
        self.length += 1
        if self.body_Direction[-1] == self.direction_Dict[0]:
            x = self.body_Positions[-1][0] - BODY_SIZE[0]
            y = self.body_Positions[-1][1]
        elif self.body_Direction[-1] == self.direction_Dict[1]:
            x = self.body_Positions[-1][0] + BODY_SIZE[0]
            y = self.body_Positions[-1][1]
        elif self.body_Direction[-1] == self.direction_Dict[2]:
            x = self.body_Positions[-1][0]
            y = self.body_Positions[-1][1] + BODY_SIZE[1]
        elif self.body_Direction[-1] == self.direction_Dict[3]:
            x = self.body_Positions[-1][0]
            y = self.body_Positions[-1][1] - BODY_SIZE[1]
        self.body_Positions.append((x, y))
        self.body_Direction.append(self.body_Direction[-1])
