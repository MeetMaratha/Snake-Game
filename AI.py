import numpy as np
import pygame
import sys
import time
from config import *


# 1. Reset Function
# 2. Reward
# 3. Play(action) -> direction
# 4. Game Iteration
# 5. Change in iscollision 


class Direction:
    def __init__(self):
        self.direction = {
            0 : "RIGHT",
            1 : "LEFT",
            2 : "UP",
            3 : "DOWN"
        }
        # self.RIGHT = 0
        # self.LEFT = 1
        # self.UP = 2
        # self.DOWN = 4
        # self.left = "LEFT"
        # self.right = "RIGHT"
        # self.up = "UP"
        # self.

class Snake:
    def __init__(self, position : tuple, length : int):

        self.head_Position = position
        self.length = length
        self.direction_Dict = Direction().direction
        self.body_Positions = [(START_POS[0], START_POS[1] - BODY_SIZE[1] * i) for i in range(self.length)]
        self.direction = self.direction_Dict[3]

    def _setDirection(self, action):
        self.direction = self.direction_Dict[action]

    def _is_Overlapping(self, new_x : int, new_y : int):
        for i in range(self.length):
            if self.head_Position == (new_x, new_y) : return True
        return False
    
    def move(self):
        for i in range(self.length - 1, 0, -1):
            self.body_Positions[i] = self.body_Positions[i - 1]
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
                self.body_Positions[0][1] - BODY_SIZE[1])
        elif self.direction == self.direction_Dict[3]:
            self.body_Positions[0] = (
                self.body_Positions[0][0], 
                self.body_Positions[0][1] + BODY_SIZE[1])
        self.head_Position = self.body_Positions[0]
        print(self.head_Position)
    
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
        if self.direction == self.direction_Dict[0]:
            x = self.body_Positions[-1][0] + BODY_SIZE[0] * self.length
            y = self.body_Positions[-1][1]
        elif self.direction == self.direction_Dict[1]:
            x = self.body_Positions[-1][0] - BODY_SIZE[0] * self.length
            y = self.body_Positions[-1][1]
        elif self.direction == self.direction_Dict[2]:
            x = self.body_Positions[-1][0]
            y = self.body_Positions[-1][0] + BODY_SIZE[1] * self.length
        elif self.direction == self.direction_Dict[3]:
            x = self.body_Positions[-1][0]
            y = self.body_Positions[-1][0] - BODY_SIZE[1] * self.length
        self.body_Positions.append((x, y))
        

class Apple:
    def __init__(self, snake : Snake):
        self.apple_Position = APPLE_START_POS

    def _appleInSnake(self, x : int ,y : int, snake : Snake):
        for i in range(snake.length):
            position = snake.body_Positions[i]
            print(position, self.apple_Position, snake.length)
            if position == (x, y) : return True
        return False

    def _getCoords(self, snake : Snake):
        x = APPLE_SIZE[0] * np.random.randint(N_WIDTH)
        y = APPLE_SIZE[1] * np.random.randint(N_HEIGHT)
        while self._appleInSnake(x, y, snake):
            x = APPLE_SIZE[0] * np.random.randint(N_WIDTH)
            y = APPLE_SIZE[1] * np.random.randint(N_HEIGHT)
        print(x, y)
        return (x, y)

class Game:
    def __init__(self, width : int, height : int, bg_Path : str, apple_Path : str, body_Path : str, ding_Path : str, crash_Path : str, title : str):
        pygame.init()
        pygame.mixer.init()
        self. width = width
        self.height = height
        self.screen = pygame.display.set_mode((self. width, self.height))
        self.background = pygame.image.load(bg_Path).convert()
        self.apple_Image = pygame.image.load(apple_Path).convert()
        self.snake_Body_Image = pygame.image.load(body_Path).convert()
        self.snake = Snake(START_POS, LENGTH)
        self.apple = Apple(self.snake)
        self.ding_Path  = ding_Path
        self.crash_Path = crash_Path
        pygame.display.set_caption(title)

    def _playBackgroundMusic(self, music_Path : str):
        pygame.mixer.music.load(music_Path)
        pygame.mixer.music.play(-1)
    
    def _playSound(self, sound_Path : str):
        sound = pygame.mixer.Sound(sound_Path)
        pygame.mixer.Sound.play(sound)

    def run(self, music_Path):
        running = True
        self._playBackgroundMusic(music_Path)
        while running:
            self.update(self.snake, self.apple)
            self._getAction()
            running = not self._isGameOver()
            if not running:
                self._closeGame()
                self._playSound(self.crash_Path)
            self.snake.move()
            if self._appleEaten():
                self.snake._increaseSnake()
                print("Okay till here")
                self._playSound(self.ding_Path)
                self.apple.apple_Position = self.apple._getCoords(self.snake)
            time.sleep(0.2)


    def update(self, snake, apple):
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        
        self.screen.blit(self.background, BG_POSITION)
        for position in self.snake.body_Positions:
            self.screen.blit(self.snake_Body_Image, position)
        self.screen.blit(self.apple_Image, self.apple.apple_Position)

        score = font.render(f"Score : {self.snake.length - 1}", True, SCORE_COLOR)
        self.screen.blit(score, SCORE_POS)
        pygame.display.flip()
    

    def _getAction(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.snake._setDirection(0)
                elif event.key == pygame.K_LEFT:
                    self.snake._setDirection(1)
                elif event.key == pygame.K_UP:
                    self.snake._setDirection(2)
                elif event.key == pygame.K_DOWN:
                    self.snake._setDirection(3)
            elif event.type == pygame.QUIT:
                self._closeGame()

    def _closeGame(self):
        font = pygame.font.SysFont(FONT_NAME, OVER_SIZE)
        game_Over = font.render(f"Game Over", True, OVER_COLOR)
        self.screen.fill(OVER_SCREEN_COLOR)
        self.screen.blit(game_Over, OVER_POS)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    def _isGameOver(self):
        if self._isWallCollison() : return True
        elif self._isBodyCollison() : return True
        else : return False

    def _isWallCollison(self):
        x_new, y_new = self.snake._getNewCoords()
        if (x_new < 0 or x_new > self.width) or (y_new < 0 and y_new > self.height) : return True
        else : return False
    
    def _isBodyCollison(self):
        (x_new, y_new) = self.snake._getNewCoords()
        if (x_new, y_new) in self.snake.body_Positions : return True
        else : return False
    
    def _appleEaten(self):
        if self.apple.apple_Position == self.snake.head_Position : return True
        else : return False


# s = Snake(START_POS[0], START_POS[1], 3)
# s._move()


if __name__ == "__main__":
    game = Game(
        width = SCREEN_WIDTH,
        height = SCREEN_HEIGHT,
        bg_Path = 'resources/background.jpg',
        apple_Path = 'resources/apple.jpg',
        body_Path = 'resources/block.jpg',
        ding_Path = 'resources/ding.mp3',
        crash_Path = 'resources/crash.mp3',
        title = TITLE
    )
    game.run('resources/bg_music_1.mp3')











# def play_sound(name : str):
#         sound = pygame.mixer.Sound(f"resources/{name}.mp3")
#         pygame.mixer.Sound.play(sound)

# class Snake:
#     def __init__(self, body_path : str, parent_screen : pygame, length : int):
#         self.length = length
#         self.body = pygame.transform.scale(pygame.image.load(body_path), BODY_SIZE)
#         self.x = [START_POS[0] for _ in range(self.length)]
#         self.y = [START_POS[1] - BODY_SIZE[0] * i for i in range(self.length)]
#         self.move = self.body.get_rect()[2]
#         self.parent_screen = parent_screen
#         self.direction = "DOWN"
    
#     def draw(self, background : pygame, width : int, height : int , apple):
        
#         self.parent_screen.blit(background, (0, 0))
#         for i in range(len(self.x)):
#             self.parent_screen.blit(self.body, (self.x[i], self.y[i]))
#         self.parent_screen.blit(apple.apple_image, (apple.x, apple.y))
#         pygame.display.flip()
    
#     def moveLeft(self):
#         self.direction = "LEFT"
    
#     def moveRight(self):
#         self.direction = "RIGHT"
    
#     def moveUp(self):
#         self.direction = "UP"
    
#     def moveDown(self):
#         self.direction = "DOWN"
    
#     def _isOverlapping(self, new_x : int, new_y : int):
#         for i in range(self.length):
#             if self.x[i] == new_x and self.y[i] == new_y:
#                 return True
#         return False
        

#     def _isCrash(self, width : int, height : int, direction : str):
#         if direction == "LEFT":
#             if self.x[0] - self.move < 0: return True
#             elif self._isOverlapping(self.x[0] - self.move, self.y[0]) : return True
#             else : return False
        
#         elif direction == "RIGHT":
#             if self.x[0] + 2*self.move > width : return True
#             elif self._isOverlapping(self.x[0] + self.move, self.y[0]) : return True
#             else : return False
            
#         elif direction == "UP":
#             if self.y[0] - self.move < 0: return True
#             elif self._isOverlapping(self.x[0], self.y[0] - self.move) : return True 
#             else : return False
        
#         elif direction == "DOWN":
#             if self.y[0] + 2*self.move > height : return True
#             elif self._isOverlapping(self.x[0], self.y[0] + self.move) : return True
#             else : return False
        
#         else : return False

        
#     def walk(self, background : pygame, width : int, height : int, apple):
#         if self._isCrash(width, height, self.direction):
#             reward = -10
#             self.displayGameOver()
#             play_sound("crash")
#             time.sleep(2)
#             return reward
#             pygame.quit()
#             sys.exit()
        
#         for i in range(self.length - 1, 0, -1):
#             self.x[i] = self.x[i - 1]
#             self.y[i] = self.y[i - 1]
        
#         if self.direction == 'LEFT':
#             self.x[0] -= self.move
        
#         if self.direction == 'RIGHT':
#             self.x[0] += self.move
        
#         if self.direction == "UP":
#             self.y[0] -= self.move
        
#         if self.direction == "DOWN":
#             self.y[0] += self.move
        

#         self.draw(background, width, height, apple)

#     def getNewCoords(self):
#         if self.direction == "DOWN":
#             self.x.append(self.x[-1])
#             self.y.append(self.y[-1] - BODY_SIZE[0] * self.length)
#         elif self.direction == "UP":
#             self.x.append(self.x[-1])
#             self.y.append(self.y[-1] + BODY_SIZE[0] * self.length)
#         elif self.direction == "LEFT":
#             self.x.append(self.x[-1] - BODY_SIZE[0] * self.length)
#             self.y.append(self.y[-1])
#         elif self.direction == "RIGHT":
#             self.x.append(self.x[-1] + BODY_SIZE[0] * self.length)
#             self.y.append(self.y[-1])

#     def displayGameOver(self):
#         font = pygame.font.SysFont('arial', 50)
#         game_over = font.render(f"Game Over", True, (255, 0, 0))
#         self.parent_screen.fill((0, 0, 0))
#         self.parent_screen.blit(game_over, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
#         pygame.display.flip()        
            

# class Apple:
#     def __init__(self, apple_path : str, screen : pygame, snake : Snake):
#         self.apple_image = pygame.transform.scale(pygame.image.load(apple_path).convert(), BODY_SIZE)
#         self.parent_screen = screen
#         self.x, self.y = self.getCoords(snake)

#     def getCoords(self, snake : Snake):
#         x = APPLE_SIZE[0] * np.random.randint(N_WIDTH)
#         y = APPLE_SIZE[1] * np.random.randint(N_HEIGHT)
#         while self.appleInSnake(x, y, snake):
#             x = APPLE_SIZE[0] * np.random.randint(N_WIDTH)
#             y = APPLE_SIZE[1] * np.random.randint(N_HEIGHT)
#         return x, y
    
#     def appleInSnake(self, x : int, y : int, snake : Snake):
#         for i in range(snake.length):
#             if snake.x[i] == x and snake.y[i] == y : return True
#         return False

#     def changeCoords(self, snake : Snake):
#         self.x, self.y = self.getCoords(snake)
    
#     def draw(self):
#         self.parent_screen.blit(self.apple_image, (self.x, self.y))




# class GameAI:
#     def __init__(self, bg_path : str, music_path : str, body_path : str, apple_path : str, width : int, height : int, length : int, epsilon : float):
#         pygame.init()
#         pygame.mixer.init()
#         self.screen = pygame.display.set_mode((width, height))
#         self.background = pygame.image.load(bg_path).convert()
#         self.snake = Snake(body_path, self.screen, length)
#         self.apple = Apple(apple_path, self.screen, self.snake)
#         self.width, self.height = width, height
#         pygame.mixer.music.load(music_path)
#         pygame.mixer.music.play(-1)
#         self.frame_iteration = 0
#         self.epsilon = epsilon
#         self.direction_dict = {
#             0 : "RIGHT",
#             1 : "LEFT",
#             2 : "UP",
#             3 : "DOWN"
#         }


#     def reset(self, body_path, apple_path, music_path):
#         self.background = pygame.image.load(bg_path).convert()
#         self.snake = Snake(body_path, self.screen, length)
#         self.apple = Apple(apple_path, self.screen, self.snake)
#         pygame.mixer.music.load(music_path)
#         pygame.mixer.music.play(-1)

#     def run(self):
#         pygame.display.set_caption('Snake')
#         running = True
#         pygame.mixer.music.play(-1)
#         self.snake.draw(self.background, self.width, self.height, self.apple)
#         while running:
#             for event in pygame.event.get():
#                 # if event.type == pygame.KEYDOWN:
#                 #     if event.key == pygame.K_UP:
#                 #         self.snake.moveUp()
#                 #     if event.key == pygame.K_DOWN:
#                 #         self.snake.moveDown()
#                 #     if event.key == pygame.K_LEFT:
#                 #         self.snake.moveLeft()
#                 #     if event.key == pygame.K_RIGHT:
#                 #         self.snake.moveRight()
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     running = False
#                     sys.exit()
            
#             action = self.get_action()
#             reward = 0
            
#             if self._isCollision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
#                 play_sound("ding")
#                 self.eaten()
#             reward = self.snake.walk(self.background, self.width, self.height, self.apple)
#             # self.apple.draw()
#             self.displayScore()
            
#             time.sleep(0.1)

#     def get_action(self, state : list, Q : np.array):
#         if np.random.rand() < epsilon:
#             action = np.random.randint(0, 4)
#         else:
#             action = np.argmax(Q[state])
#         return self.direction_dict[action]

#     def _isCollision(self, x1 : int, y1 : int, x2 : int, y2 : int):
#         if self.snake.direction == "DOWN":
#             if x1 == x2 and y2 - y1 == 0 : return True
#             else : return False
#         elif self.snake.direction == "UP":
#             if x1 == x2 and y1 - (y2 + APPLE_SIZE[0]) == 0 : return True
#             else : return False
#         elif self.snake.direction == "LEFT":
#             if y1 == y2 and x1 - (x2 + APPLE_SIZE[0]) == 0 : return True
#             else : return False
#         elif self.snake.direction == "RIGHT":
#             if y1 == y2 and x2 - x1 == 0 : return True
#             else : return False

#     def eaten(self):
#         self.apple.changeCoords(self.snake)
#         self.snake.length += 1
#         self.snake.getNewCoords()
    
#     def displayScore(self):
#         font = pygame.font.SysFont('arial', 20)
#         score = font.render(f"Score : {self.snake.length - 1}", True, (255, 255, 255))
#         self.screen.blit(score, SCORE_POS)
#         pygame.display.flip()                
