import pygame
import sys
from settings import *
from snake import Snake

pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

def game_loop():
    game_over = False
    game_close = False
    
    while not game_over:
        
        
        screen.fill(BLUE)
        pygame.display.update()
    
        clock.tick(SNAKE_SPEED)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
