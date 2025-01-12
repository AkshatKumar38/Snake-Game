import pygame
import sys
from settings import *
from snake import Snake
from food import Food

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Fonts
FONT_PATH = "assets/fonts/arcade_font.ttf"
font_style = pygame.font.Font(FONT_PATH, 25)
score_font = pygame.font.Font(FONT_PATH, 35)

def display_score(score):
    value = score_font.render(f"Score: {score}", True, WHITE)
    # Place the score inside the playable area
    screen.blit(value, (PLAYABLE_X_OFFSET + 10, PLAYABLE_Y_OFFSET - 40))

def message(text, color, position):
    msg = font_style.render(text, True, color)
    screen.blit(msg, position)

def draw_borders():
    pygame.draw.rect(screen, YELLOW, (PLAYABLE_X_OFFSET, PLAYABLE_Y_OFFSET, PLAYABLE_WIDTH, PLAYABLE_HEIGHT), 5)  # Border thickness is 5

def start_screen():
    screen.fill(BLACK)
    message("Welcome to Snake Game!", WHITE, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3))
    message("Press SPACE to Start", WHITE, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def game_loop():
    game_over = False
    game_close = False

    snake = Snake()
    food = Food()

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message("You Lost! Press Q-Quit or C-Play Again", RED, (SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3))
            display_score(len(snake.body) - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")

        snake.move()

        # Check for collisions with walls
        head = snake.body[0]
        if (
            head[0] == PLAYABLE_X_OFFSET or 
            head[0] == PLAYABLE_X_OFFSET + PLAYABLE_WIDTH - BLOCK_SIZE or
            head[1] == PLAYABLE_Y_OFFSET or 
            head[1] == PLAYABLE_Y_OFFSET + PLAYABLE_HEIGHT - BLOCK_SIZE
        ):
            game_close = True


        # Check for collisions with itself
        if head in snake.body[1:]:
            game_close = True

        # Check if snake eats food
        if head == food.position:
            snake.eat_food()
            food.relocate()

        screen.fill(BLUE)
        draw_borders()
        snake.draw(screen, GREEN)
        food.draw(screen, RED)
        display_score(len(snake.body) - 1)
        pygame.display.update()

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_screen()
    game_loop()
