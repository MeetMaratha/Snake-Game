import numpy as np
import pygame
import sys

class Snake:
    def __init__(self, bg_path, music_path, body_path, width, height):
        pygame.init()
        self.background = pygame.image.load(bg_path)
        self.width = width
        self.height = height
        self.music = pygame.mixer.music.load(music_path)
        self.body = pygame.image.load(body_path)
        self.body_position = [np.random.randint(self.width), np.random.randint(self.height)]
        self.move = self.body.get_rect()[3]

    def run(self):
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')
        running = True
        pygame.mixer.music.play(-1)
        while running:
            screen.blit(self.background, (0, 0))
            screen.blit(self.body, self.body_position)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.body_position[1] - self.move > 0 : self.body_position[1] -= self.move
                        else : self.body_position[1] = self.height - self.move 
                    if event.key == pygame.K_DOWN:
                        if self.body_position[1] + self.move < self.height : self.body_position[1] += self.move
                        else : self.body_position[1] = 0
                    if event.key == pygame.K_LEFT:
                        if self.body_position[0] - self.move > 0 : self.body_position[0] -= self.move
                        else : self.body_position[0] = self.width - self.move
                    if event.key == pygame.K_RIGHT:
                        if self.body_position[0] + self.move < self.width : self.body_position[0] += self.move
                        else : self.body_position[0] = 0
                if event.type == pygame.QUIT:
                    # sys.exit()
                    pygame.quit()
                    running = False
    
if __name__ == "__main__":
    s = Snake(
        bg_path = 'resources/background.jpg',
        music_path = 'resources/bg_music_1.mp3',
        body_path = 'resources/block.jpg',
        width = 640,
        height = 480
    )
    s.run()