# Snake class to manage the snake's behavior
import pygame

class Snake:
    def __init__(self):
        self.body = [[400,300]]
        self.direction = "RIGHT"
        self.grow = False
        
    # def move(self):
    #     head = self.body[0]
    #     if self.direction == "UP":
    #         new_head = 
    #     if self.direction == "DOWN":
    #         new_head = 
    #     if self.direction == "LEFT":
    #         new_head = 
    #     if self.direction == "RIGHT":
    #         new_head = 