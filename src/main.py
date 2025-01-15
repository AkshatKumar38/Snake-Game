import pygame, math, numpy as np
import sys
from score import *
from settings import *
from snake import Snake
from food import Food
from snakeAI import SnakeAI
from plot import PlotThread

pygame.init()
pygame.display.set_caption("Snake Game")

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
    # Create Q-learning agent
    state_size = (PLAYABLE_X_OFFSET, PLAYABLE_Y_OFFSET)  # Define state size (customize as needed)
    action_size = len(actions)
    ai = SnakeAI(state_size, action_size)


    rewards_per_episode = []
    epsilons_per_episode = []
    avg_q_values_per_episode = []

    # Run the game using the trained AI
    running = True  # Continuous gameplay
    while running:
        snake.__init__()  # Reset snake for a new game
        food.relocate()  # Relocate food
        total_reward = 0  # Track total reward for the current game
        game_over = False

        while not game_over:
            # Get the current state
            state = ai.encode_state(snake,food)
            
            # AI chooses an action
            action_idx = ai.choose_action(state)
            action = actions[action_idx]
            snake.change_direction(action)
            snake.move()
            
            # Check for collisions and rewards
            head = snake.body[0]
            reward = 0
            if head == food.position:
                reward = 50  # Snake eats food
                snake.eat_food()
                food.relocate()
            elif (
                head in snake.body[1:]
                or head[0] < PLAYABLE_X_OFFSET
                or head[0] >= PLAYABLE_X_OFFSET + PLAYABLE_WIDTH
                or head[1] < PLAYABLE_Y_OFFSET
                or head[1] >= PLAYABLE_Y_OFFSET + PLAYABLE_HEIGHT
            ):
                reward = -100  # Game over due to collision
                game_over = True
            else:
                # Encourage moving closer to food
                old_distance = math.sqrt((head[0] - food.position[0])**2 + (head[1] - food.position[1])**2)
                new_distance = math.sqrt((snake.body[0][0] - food.position[0])**2 + (snake.body[0][1] - food.position[1])**2)
                distance_reward = 10 * (old_distance - new_distance)
                reward = max(-1, distance_reward)

            total_reward += reward

            # Update the AI with the new experience
            next_state = ai.encode_state(snake, food)  # Update state after action
            ai.update_q_table(state, action_idx, reward, next_state, game_over)
            
            # Update screen for AI play
            screen.fill(BLUE)
            draw_background()
            draw_borders()
            snake.draw(screen, GREEN)
            food.draw(screen, RED)

            pygame.display.update()
            clock.tick(SNAKE_SPEED)

        # Decay exploration rate after each episode
        ai.decay_exploration_rate()
        
        # Track metrics
        avg_q_value = np.mean([ai.get_q_value(state, a) for a in range(action_size)])
        rewards_per_episode.append(total_reward)
        epsilons_per_episode.append(ai.exploration_rate)
        avg_q_values_per_episode.append(avg_q_value)
        #plot_thread.update_data(rewards_per_episode, epsilons_per_episode, avg_q_values_per_episode)
        # Print the values to the console instead of plotting them
        print(f"Episode {len(rewards_per_episode)}:")
        print(f"  Total Reward: {total_reward}")
        print(f"  Exploration Rate (Epsilon): {ai.exploration_rate}")
        print(f"  Average Q-value: {avg_q_value:.4f}")
        print("-" * 40)
        # Check if the user wants to quit or continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    # Stop the plot thread when the game finishes

    pygame.quit()

def game_loop(mode):
    if mode == "player":
        player_game_loop()  # Player game logic
    elif mode == "ai":
        ai_game_loop()  # AI game logic

if __name__ == "__main__":
    mode = start_screen()
    game_loop(mode)
