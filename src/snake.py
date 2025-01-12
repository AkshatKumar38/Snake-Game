import pygame
from settings import *

class Snake:
    def __init__(self):
        self.body = [[PLAYABLE_X_OFFSET + 400, PLAYABLE_Y_OFFSET + 300]]  # Initial position
        self.direction = "RIGHT"
        self.grow = False

    def move(self):
        head = self.body[0]
        if self.direction == "UP":
            new_head = [head[0], head[1] - BLOCK_SIZE]
        elif self.direction == "DOWN":
            new_head = [head[0], head[1] + BLOCK_SIZE]
        elif self.direction == "LEFT":
            new_head = [head[0] - BLOCK_SIZE, head[1]]
        else:  # RIGHT
            new_head = [head[0] + BLOCK_SIZE, head[1]]

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        self.grow = False

    def change_direction(self, new_direction):
        opposite_directions = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def eat_food(self):
        self.grow = True

    def draw(self, screen, color):
        for segment in self.body:
            pygame.draw.rect(screen, color, (*segment, BLOCK_SIZE, BLOCK_SIZE))