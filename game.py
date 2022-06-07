import numpy as np
import pygame
import sys
import time
from config import *


def play_sound(name : str):
        sound = pygame.mixer.Sound(f"resources/{name}.mp3")
        pygame.mixer.Sound.play(sound)

class Snake:
    def __init__(self, body_path : str, parent_screen : pygame, length : int):
        self.length = length
        self.body = pygame.transform.scale(pygame.image.load(body_path), BODY_SIZE)
        self.x = [START_POS[0] for _ in range(self.length)]
        self.y = [START_POS[1] - BODY_SIZE[0] * i for i in range(self.length)]
        self.move = self.body.get_rect()[2]
        self.parent_screen = parent_screen
        self.direction = "DOWN"
    
    def draw(self, background : pygame, width : int, height : int , apple):
        
        self.parent_screen.blit(background, (0, 0))
        for i in range(len(self.x)):
            self.parent_screen.blit(self.body, (self.x[i], self.y[i]))
        self.parent_screen.blit(apple.apple_image, (apple.x, apple.y))
        pygame.display.flip()
    
    def moveLeft(self):
        self.direction = "LEFT"
    
    def moveRight(self):
        self.direction = "RIGHT"
    
    def moveUp(self):
        self.direction = "UP"
    
    def moveDown(self):
        self.direction = "DOWN"
    
    def _isOverlapping(self, new_x : int, new_y : int):
        for i in range(self.length):
            if self.x[i] == new_x and self.y[i] == new_y:
                return True
        return False
        

    def _isCrash(self, width : int, height : int, direction : str):
        if direction == "LEFT":
            if self.x[0] - self.move < 0: return True
            elif self._isOverlapping(self.x[0] - self.move, self.y[0]) : return True
            else : return False
        
        elif direction == "RIGHT":
            if self.x[0] + 2*self.move > width : return True
            elif self._isOverlapping(self.x[0] + self.move, self.y[0]) : return True
            else : return False
            
        elif direction == "UP":
            if self.y[0] - self.move < 0: return True
            elif self._isOverlapping(self.x[0], self.y[0] - self.move) : return True 
            else : return False
        
        elif direction == "DOWN":
            if self.y[0] + 2*self.move > height : return True
            elif self._isOverlapping(self.x[0], self.y[0] + self.move) : return True
            else : return False
        
        else : return False

        
    def walk(self, background : pygame, width : int, height : int, apple):
        if self._isCrash(width, height, self.direction):
            self.displayGameOver()
            play_sound("crash")
            time.sleep(2)
            pygame.quit()
            sys.exit()
        
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        
        if self.direction == 'LEFT':
            self.x[0] -= self.move
        
        if self.direction == 'RIGHT':
            self.x[0] += self.move
        
        if self.direction == "UP":
            self.y[0] -= self.move
        
        if self.direction == "DOWN":
            self.y[0] += self.move
        

        self.draw(background, width, height, apple)

    def getNewCoords(self):
        if self.direction == "DOWN":
            self.x.append(self.x[-1])
            self.y.append(self.y[-1] - BODY_SIZE[0] * self.length)
        elif self.direction == "UP":
            self.x.append(self.x[-1])
            self.y.append(self.y[-1] + BODY_SIZE[0] * self.length)
        elif self.direction == "LEFT":
            self.x.append(self.x[-1] - BODY_SIZE[0] * self.length)
            self.y.append(self.y[-1])
        elif self.direction == "RIGHT":
            self.x.append(self.x[-1] + BODY_SIZE[0] * self.length)
            self.y.append(self.y[-1])

    def displayGameOver(self):
        font = pygame.font.SysFont('arial', 50)
        game_over = font.render(f"Game Over", True, (255, 0, 0))
        self.parent_screen.fill((0, 0, 0))
        self.parent_screen.blit(game_over, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
        pygame.display.flip()        
            

class Apple:
    def __init__(self, apple_path : str, screen : pygame, snake : Snake):
        self.apple_image = pygame.transform.scale(pygame.image.load(apple_path).convert(), BODY_SIZE)
        self.parent_screen = screen
        self.x, self.y = self.getCoords(snake)

    def getCoords(self, snake : Snake):
        x = APPLE_SIZE[0] * np.random.randint(N_WIDTH)
        y = APPLE_SIZE[1] * np.random.randint(N_HEIGHT)
        while self.appleInSnake(x, y, snake):
            x = APPLE_SIZE[0] * np.random.randint(N_WIDTH)
            y = APPLE_SIZE[1] * np.random.randint(N_HEIGHT)
        return x, y
    
    def appleInSnake(self, x : int, y : int, snake : Snake):
        for i in range(snake.length):
            if snake.x[i] == x and snake.y[i] == y : return True
        return False

    def changeCoords(self, snake : Snake):
        self.x, self.y = self.getCoords(snake)
    
    def draw(self):
        self.parent_screen.blit(self.apple_image, (self.x, self.y))




class Game:
    def __init__(self, bg_path : str, music_path : str, body_path : str, apple_path : str, width : int, height : int, length : int):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height))
        self.background = pygame.image.load(bg_path).convert()
        self.snake = Snake(body_path, self.screen, length)
        self.apple = Apple(apple_path, self.screen, self.snake)
        self.width, self.height = width, height
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

    def run(self):
        pygame.display.set_caption('Snake')
        running = True
        pygame.mixer.music.play(-1)
        self.snake.draw(self.background, self.width, self.height, self.apple)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.moveUp()
                    if event.key == pygame.K_DOWN:
                        self.snake.moveDown()
                    if event.key == pygame.K_LEFT:
                        self.snake.moveLeft()
                    if event.key == pygame.K_RIGHT:
                        self.snake.moveRight()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    sys.exit()
            
            if self._isCollision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
                play_sound("ding")
                self.eaten()
            self.snake.walk(self.background, self.width, self.height, self.apple)
            # self.apple.draw()
            self.displayScore()
            
            time.sleep(0.1)

    def _isCollision(self, x1 : int, y1 : int, x2 : int, y2 : int):
        if self.snake.direction == "DOWN":
            if x1 == x2 and y2 - y1 == 0 : return True
            else : return False
        elif self.snake.direction == "UP":
            if x1 == x2 and y1 - (y2 + APPLE_SIZE[0]) == 0 : return True
            else : return False
        elif self.snake.direction == "LEFT":
            if y1 == y2 and x1 - (x2 + APPLE_SIZE[0]) == 0 : return True
            else : return False
        elif self.snake.direction == "RIGHT":
            if y1 == y2 and x2 - x1 == 0 : return True
            else : return False

    def eaten(self):
        self.apple.changeCoords(self.snake)
        self.snake.length += 1
        self.snake.getNewCoords()
    
    def displayScore(self):
        font = pygame.font.SysFont('arial', 20)
        score = font.render(f"Score : {self.snake.length - 1}", True, (255, 255, 255))
        self.screen.blit(score, SCORE_POS)
        pygame.display.flip()                
