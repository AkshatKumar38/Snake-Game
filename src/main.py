import pygame, math
import sys
from score import *
from settings import *
from snake import Snake
from food import Food
from snakeAI import SnakeAI

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Fonts
FONT_PATH = "assets/fonts/arcade_font.ttf"
font_style = pygame.font.Font(FONT_PATH, 25)
score_font = pygame.font.Font(FONT_PATH, 35)


def start_screen():
    screen.fill(BLACK)
    message("Welcome to Snake Game!", WHITE, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3))
    message("Press P to Play as Player", WHITE, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2))
    message("Press A to Let AI Play", WHITE, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 1.8))
    pygame.display.update()

    waiting = True
    mode = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    mode = "player"
                    waiting = False
                elif event.key == pygame.K_a:
                    mode = "ai"
                    waiting = False
    return mode            

def player_game_loop():
    game_over = False
    game_close = False

    snake = Snake()
    food = Food()
    high_score = get_high_score()

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message("You Lost! Press Q-Quit or C-Play Again", RED, (SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3))
            display_score(len(snake.body) - 1, high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        current_score = len(snake.body) - 1
                        update_high_score(current_score)
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        snake = Snake()
                        food = Food()
                        game_close = False

        # Player control loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                current_score = len(snake.body) - 1
                update_high_score(current_score)
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

        # Check collisions with walls
        head = snake.body[0]
        if (
            head[0] < PLAYABLE_X_OFFSET or
            head[0] >= PLAYABLE_X_OFFSET + PLAYABLE_WIDTH or
            head[1] < PLAYABLE_Y_OFFSET or
            head[1] >= PLAYABLE_Y_OFFSET + PLAYABLE_HEIGHT
        ):
            game_close = True

        # Check if snake eats food
        if head == food.position:
            snake.eat_food()
            food.relocate()

        # Update the screen
        screen.fill(BLUE)
        draw_background()
        draw_borders()
        snake.draw(screen, GREEN)
        food.draw(screen, RED)
        current_score = len(snake.body) - 1
        if current_score > high_score:
            high_score = current_score
        display_score(current_score, high_score)

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

    update_high_score(len(snake.body) - 1)
    pygame.quit()
    sys.exit()

# Main game loop for AI to play
def ai_game_loop():
    snake = Snake()
    food = Food()
    actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    ai = SnakeAI(snake, food, actions)
    
    # Train the AI
    ai.train(num_episodes=5000)

    # Run the game for a specified number of iterations
    num_iterations = 100  # Number of iterations per episode
    for episode in range(1000):  # Loop through episodes
        game_over = False
        snake.__init__()  # Reset snake for a new episode
        food.relocate()  # Relocate food for a new episode
        total_reward = 0  # Track total reward for current episode
        
        while not game_over and num_iterations > 0:
            print(f"Inside interation loop {episode + 1}, Current interation {num_iterations}")
            # AI game logic: AI decides the action and moves the snake
            state = ai.get_state()
            action = ai.choose_action(state)
            snake.change_direction(action)
            snake.move()

            # Check for collisions and rewards
            head = snake.body[0]
            reward = 0
            if head == food.position:
                reward = 50  # Snake eats food
                snake.eat_food()
                food.relocate()  # Respawn food
            elif head in snake.body[1:] or head[0] < PLAYABLE_X_OFFSET or head[0] >= PLAYABLE_X_OFFSET + PLAYABLE_WIDTH or head[1] < PLAYABLE_Y_OFFSET or head[1] >= PLAYABLE_Y_OFFSET + PLAYABLE_HEIGHT:
                reward = -100  # Game over due to collision
                game_over = True
            else:
                # Encourage moving closer to food
                old_distance = math.sqrt((head[0] - food.position[0])**2 + (head[1] - food.position[1])**2)
                new_distance = math.sqrt((snake.body[0][0] - food.position[0])**2 + (snake.body[0][1] - food.position[1])**2)
                distance_reward = 10 * (old_distance - new_distance)  # Positive for getting closer, negative for moving away
                reward = max(-1, distance_reward)
                # Penalize wasting time
                
            
            total_reward += reward
            
            # Reset if total reward falls below -50
            if total_reward < -100:
                break
            # Update AI Q-values
            next_state = ai.get_state()
            ai.update_q_value(state, action, reward, next_state)
            # Update screen for AI play
            screen.fill(BLUE)
            draw_background()
            draw_borders()
            snake.draw(screen, GREEN)
            food.draw(screen, RED)
            
            # Display stats on the side
            avg_q_value = sum(ai.q_values[state].values()) / len(ai.q_values[state]) if state in ai.q_values else 0
            display_stats(screen, episode, total_reward, ai.epsilon, ai.alpha, ai.gamma, avg_q_value)

            pygame.display.update()
            clock.tick(SNAKE_SPEED)
            num_iterations -= 1  # Decrease number of iterations left for the episode
            if num_iterations == 0:  # If all iterations for the episode are done
                break  # Break out of the while loop for the current episode

        num_iterations = 100  # Reset iterations for the next episode

    pygame.quit()

def game_loop(mode):
    if mode == "player":
        player_game_loop()  # Player game logic
    elif mode == "ai":
        ai_game_loop()  # AI game logic

if __name__ == "__main__":
    mode = start_screen()
    game_loop(mode)
