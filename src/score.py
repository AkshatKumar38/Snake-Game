import os, pygame
from settings import *
from main import font_style, score_font

# High Score File Path
HIGH_SCORE_FILE = "highscore.txt"

# Draw the background of the playable area
def draw_background():
    pygame.draw.rect(screen, BLACK, (PLAYABLE_X_OFFSET, PLAYABLE_Y_OFFSET, PLAYABLE_WIDTH, PLAYABLE_HEIGHT))

def draw_borders():
    pygame.draw.rect(screen, YELLOW, (PLAYABLE_X_OFFSET, PLAYABLE_Y_OFFSET, PLAYABLE_WIDTH, PLAYABLE_HEIGHT), 5)

def get_high_score():
    try:
        if not os.path.exists(HIGH_SCORE_FILE):
            return 0
        with open(HIGH_SCORE_FILE, "r") as file:
            high_score = int(file.read().strip())
            return high_score
    except (ValueError, FileNotFoundError):
        print("Error reading high score file. Returning 0.")
        return 0

def update_high_score(score):
    try:
        high_score = get_high_score()
        if score > high_score:
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write(str(score))
                file.flush()  # Ensure data is written to disk
    except Exception as e:
        print(f"Error updating high score: {e}")

def display_score(score, high_score):
    score_text = score_font.render(f"Your Score: {score}", True, WHITE)
    high_score_text = score_font.render(f"High Score: {high_score}", True, WHITE)

    # Display above playable area
    screen.blit(score_text, (PLAYABLE_X_OFFSET + 10, PLAYABLE_Y_OFFSET - 60))
    screen.blit(high_score_text, (PLAYABLE_X_OFFSET + 480, PLAYABLE_Y_OFFSET - 60))

def message(text, color, position):
    msg = font_style.render(text, True, color)
    screen.blit(msg, position)
    