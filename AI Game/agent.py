import torch
import numpy as np
from AI import GameAI
from collections import deque
from config import *
from model import Linear_QNet, QTrainer
from helper import plot
import random


def Point(position : tuple, change : tuple, difference : int):
    '''
    Position : Position to use
    change : (x_Change, y_Change), positive to add, negative to subtract
    difference : Amount of difference
    ''' 
    pos = [0, 0]
    pos[0] = position[0] + change[0] * difference if change[0] != 0 else position[0]
    pos[1] = position[1] + change[1] * difference if change[1] != 0 else position[1] 

    return tuple(pos)

class Agent:
    def __init__(self):
        self.n_Games = 0
        self.epsilon = 0
        self.gamma = GAMMA
        self.memory = deque(maxlen = MAX_MEMORY) # Queue
        self.model = Linear_QNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
        self.trainer = QTrainer(self.model, LR, self.gamma)


    def getState(self, game : GameAI) -> np.array:
        head_Position = game.snake.head_Position
        
        point_L = Point(head_Position, (-1, 0), BODY_SIZE[0])
        point_R = Point(head_Position, (1, 0), BODY_SIZE[0])
        point_U = Point(head_Position, (0, -1), BODY_SIZE[1])
        point_D = Point(head_Position, (0, 1), BODY_SIZE[1])

        dir_R = game.snake.direction == game.snake.direction_Dict[0]
        dir_L = game.snake.direction == game.snake.direction_Dict[1]
        dir_U = game.snake.direction == game.snake.direction_Dict[2]
        dir_D = game.snake.direction == game.snake.direction_Dict[3]

        state = [
            # Danger straight
            (dir_R and (game._isWallCollison(point_R) or game._isBodyCollison(point_R))) or
            (dir_L and (game._isWallCollison(point_L) or game._isBodyCollison(point_L))) or
            (dir_U and (game._isWallCollison(point_U) or game._isBodyCollison(point_U))) or
            (dir_D and (game._isWallCollison(point_D) or game._isBodyCollison(point_D))),

            # Danger Right
            (dir_R and (game._isWallCollison(point_D) or game._isBodyCollison(point_D))) or
            (dir_L and (game._isWallCollison(point_U) or game._isBodyCollison(point_U))) or
            (dir_U and (game._isWallCollison(point_R) or game._isBodyCollison(point_R))) or
            (dir_D and (game._isWallCollison(point_L) or game._isBodyCollison(point_L))),

            # Danger Left
            (dir_R and (game._isWallCollison(point_U) or game._isBodyCollison(point_U))) or
            (dir_L and (game._isWallCollison(point_D) or game._isBodyCollison(point_D))) or
            (dir_U and (game._isWallCollison(point_L) or game._isBodyCollison(point_L))) or
            (dir_D and (game._isWallCollison(point_R) or game._isBodyCollison(point_R))),

            # Moving direction
            dir_L,
            dir_R,
            dir_U,
            dir_D,

            # Food Location
            head_Position[0] < game.apple.apple_Position[0], # Food Left
            head_Position[0] > game.apple.apple_Position[0], # Food Right
            head_Position[1] < game.apple.apple_Position[1], # Food Up
            head_Position[1] > game.apple.apple_Position[1] # Food Down
        ]

        return np.array(state, dtype = int)

    
    def remember(self, state : list, action : int, reward : int, next_state : list, done : int):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def trainLongMemory(self):
        '''
        We train again all the memory we have collected. We train on BATCH_SIZE length of data for this
        '''
        mini_sample = random.sample(self.memory, BATCH_SIZE) if len(self.memory) > BATCH_SIZE else self.memory # BATCH_SIZE number of tuples
        print(len(mini_sample))
        states, actions, rewards, next_states, dones = zip(*mini_sample) # easy way to extract


        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
        


    def trainShortMemory(self, state : list, action : int, reward : int, next_state : list, done : int):
        self.trainer.train_step(state, action, reward, next_state, done)

    def getAction(self, state : list):
        # What action to take?
        self.epsilon = EPSILON - self.n_Games
        action = [0, 0, 0]
        if np.random.randint(0, 1000) < self.epsilon:
            move = np.random.randint(0, 2)
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
        action[move] = 1
        return action

def train():
    plot_Scores = []
    plot_Mean_Scores = []
    total_Score = 0
    record = 0
    agent = Agent()
    game = GameAI(
        width = SCREEN_WIDTH,
        height = SCREEN_HEIGHT,
        bg_Path = '../resources/background.jpg',
        apple_Path = '../resources/apple.jpg',
        body_Path = '../resources/block.jpg',
        ding_Path = '../resources/ding.mp3',
        crash_Path = '../resources/crash.mp3',
        music_Path = '../resources/bg_music_1.mp3',
        title = TITLE
    )
    while True:
        # get Old state
        state_old = agent.getState(game)

        # Get move
        action = agent.getAction(state_old)

        # perform move and get new state
        reward, done, score = game.runAI(action)
        state_new = agent.getState(game)

        # train short memory
        agent.trainShortMemory(state_old, action, reward, state_new, done)

        # Remember
        agent.remember(state_old, action, reward, state_new, done)

        if done:
            # Train long memory, plot results
            game.reset()
            agent.n_Games += 1
            agent.trainLongMemory()

            if score > record:
                record = score
                agent.model.save()

            print(f'Game : {agent.n_Games} | Score : {score} | Record : {record}')

            plot_Scores.append(score)
            total_Score += score
            mean_Score = total_Score / agent.n_Games
            plot_Mean_Scores.append(mean_Score)
            plot(plot_Scores, plot_Mean_Scores)


if __name__ == "__main__":
    train()
