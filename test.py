import pygame
import os  # To handle file paths


# Path to the font
FONT_PATH = os.path.join("..", "assets", "fonts", "arcade_font.ttf")

cusstom = pygame.font.Font(FONT_PATH())

print(cusstom)