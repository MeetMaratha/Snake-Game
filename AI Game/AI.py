import numpy as np
import pygame
import sys
import time
from config import *
from snake import Snake
from apple import Apple

# TODO : 
# 1. Reset Function
# 2. Reward
# 3. Play(action) -> direction
# 4. Game Iteration
# 5. Change in iscollision 




        


class GameAI:
    def __init__(self, width : int, height : int, bg_Path : str, apple_Path : str, body_Path : str, ding_Path : str, crash_Path : str, music_Path : str, title : str):
        pygame.init()
        pygame.mixer.init()
        self. width = width
        self.height = height
        self.screen = pygame.display.set_mode((self. width, self.height))
        self.background = pygame.image.load(bg_Path).convert()
        self.apple_Image = pygame.image.load(apple_Path).convert()
        self.snake_Body_Image = pygame.image.load(body_Path).convert()
        self.snake = Snake(
            (BODY_SIZE[0] * np.random.randint(N_WIDTH), BODY_SIZE[1] * np.random.randint(N_HEIGHT)), 
            LENGTH)
        self.apple = Apple(self.snake)
        self.ding_Path  = ding_Path
        self.crash_Path = crash_Path
        self.score = 0
        pygame.display.set_caption(title)
        self.frame_Iteration = 0
        self._playBackgroundMusic(music_Path)

    def _playBackgroundMusic(self, music_Path : str):
        pygame.mixer.music.load(music_Path)
        pygame.mixer.music.play(-1)
    
    def _playSound(self, sound_Path : str):
        sound = pygame.mixer.Sound(sound_Path)
        pygame.mixer.Sound.play(sound)

    # def run(self, music_Path):
    #     running = True
    #     self._playBackgroundMusic(music_Path)
    #     while running:
    #         self.frame_Iteration += 1
    #         time.sleep(0.13)
    #         self.update(self.snake, self.apple)
    #         action = self._getActionAI()
    #         reward = 0
    #         running = not self._isGameOver()
    #         if not running or self.frame_Iteration > 100 * self.snake.length:
    #             reward = OVER_REWARD
    #             self._closeGame()
    #         self._setSnakeDirection(action)
    #         self.snake.move()
    #         if self._appleEaten():
    #             self.score += 1
    #             reward = EATEN_REWARD
    #             self.snake._increaseSnake()
    #             self._playSound(self.ding_Path)
    #             self.apple.apple_Position = self.apple._getCoords(self.snake)



    def update(self, snake, apple):
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        
        self.screen.blit(self.background, BG_POSITION)
        for position in self.snake.body_Positions:
            self.screen.blit(self.snake_Body_Image, position)
        self.screen.blit(self.apple_Image, self.apple.apple_Position)

        score = font.render(f"Score : {self.score}", True, SCORE_COLOR)
        self.screen.blit(score, SCORE_POS)
        pygame.display.flip()
    
    # Removed to make game work using AI

    # def _getAction(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_RIGHT:
    #                 self.snake._setDirection(0)
    #             elif event.key == pygame.K_LEFT:
    #                 self.snake._setDirection(1)
    #             elif event.key == pygame.K_UP:
    #                 self.snake._setDirection(2)
    #             elif event.key == pygame.K_DOWN:
    #                 self.snake._setDirection(3)
    #         elif event.type == pygame.QUIT:
    #             self._closeGame()

    def _closeGame(self):
        font = pygame.font.SysFont(FONT_NAME, OVER_SIZE)
        game_Over = font.render(f"Game Over", True, OVER_COLOR)
        pygame.mixer.music.stop()
        self._playSound(self.crash_Path)
        self.screen.fill(OVER_SCREEN_COLOR)
        self.screen.blit(game_Over, OVER_POS)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    def _isGameOver(self):
        if self._isWallCollison() or self._isBodyCollison(): return True
        else : return False

    def _isWallCollison(self, position : tuple = None):
        x, y = self.snake.head_Position if position == None else position
        if x < 0 or x + BODY_SIZE[0] > self.width : return True
        elif y < 0 or y + BODY_SIZE[1] > self.height : return True
        else : return False
    
    def _isBodyCollison(self, position : tuple = None):
        (x_new, y_new) = self.snake._getNewCoords() if position == None else position 
        if (x_new, y_new) in self.snake.body_Positions : return True
        else : return False
    
    def _appleEaten(self):
        if self.apple.apple_Position == self.snake.head_Position : return True
        else : return False

    # Coding for making it work with AI
    def reset(self):
        self.snake = Snake(
            (BODY_SIZE[0] * np.random.randint(N_WIDTH), BODY_SIZE[1] * np.random.randint(N_HEIGHT)), 
            LENGTH)
        self.apple = Apple(self.snake)
        self.score = 0
        self.frame_Iteration = 0        

    def _getKeyAI(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._closeGame()
    
    def _setSnakeDirection(self, action):
        clock_wise = [
            self.snake.direction_Dict[0], #  Right
            self.snake.direction_Dict[3], #  Down
            self.snake.direction_Dict[1], #  Left
            self.snake.direction_Dict[2]  #  Up
        ]
        idx = clock_wise.index(self.snake.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]    # No Change

        elif np.array_equal(action, [0, 1, 0]):
            idx = (idx + 1) % 4
            new_dir = clock_wise[idx] # Turn Right R -> D -> L -> U
        
        elif np.array_equal(action, [0, 0, 1]):
            idx = (idx - 1) % 4
            new_dir = clock_wise[idx] # Turn Left R -> U -> L -> D
        self.snake.direction = new_dir
    
    def runAI(self, action):
        # running = True
        self.frame_Iteration += 1
        # time.sleep(0.2)
        self._getKeyAI()
        reward = 0
        done = self._isGameOver()
        if done or self.frame_Iteration > 100 * self.snake.length:
            done = True
            reward = OVER_REWARD
            print(reward)
            # self._closeGame()
        self._setSnakeDirection(action)
        self.snake.move()
        if self._appleEaten():
            self.score += 1
            reward = EATEN_REWARD
            self.snake._increaseSnake()
            self._playSound(self.ding_Path)
            self.apple.apple_Position = self.apple._getCoords(self.snake)

        self.update(self.snake, self.apple)
        return reward, done, self.score
