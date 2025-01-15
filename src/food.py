# Food class to manage the food behavior
import pygame
import random
from settings import *

class Food:
    def __init__(self):
        self.position = [
            random.randrange(0, PLAYABLE_WIDTH, BLOCK_SIZE) + PLAYABLE_X_OFFSET,
            random.randrange(0, PLAYABLE_HEIGHT, BLOCK_SIZE) + PLAYABLE_Y_OFFSET
        ]

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (*self.position, BLOCK_SIZE, BLOCK_SIZE))

    def relocate(self):
        self.position = [
            random.randrange(0, PLAYABLE_WIDTH, BLOCK_SIZE) + PLAYABLE_X_OFFSET,
            random.randrange(0, PLAYABLE_HEIGHT, BLOCK_SIZE) + PLAYABLE_Y_OFFSET
        ]