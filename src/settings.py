# Game settings and constants
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
SNAKE_SPEED = 50

# Playable area dimensions
PLAYABLE_WIDTH = 800
PLAYABLE_HEIGHT = 600

# Centered playable area position
PLAYABLE_X_OFFSET = (SCREEN_WIDTH - PLAYABLE_WIDTH) // 2
PLAYABLE_Y_OFFSET = (SCREEN_HEIGHT - PLAYABLE_HEIGHT) // 2

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT_PATH = "assets/fonts/arcade_font.ttf"
clock = pygame.time.Clock()