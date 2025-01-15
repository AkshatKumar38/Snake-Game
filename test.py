import pygame
import random
import time

# Assuming other necessary constants and classes (e.g., Snake, Food, etc.) are defined elsewhere in the code

class SnakeAI:
    def __init__(self, snake, food, actions, screen):
        self.snake = snake
        self.food = food
        self.actions = actions
        self.q_values = {}
        self.epsilon = 0.3  # Exploration rate
        self.alpha = 0.1    # Learning rate
        self.gamma = 0.9    # Discount factor
        self.screen = screen  # Pygame screen object for rendering progress

    def get_state(self):
        # The state is represented by the snake's head position and food position
        return (self.snake.body[0], self.food.position)

    def choose_action(self, state):
        # Initialize state if it does not exist in q_values
        if state not in self.q_values:
            self.q_values[state] = {action: 0 for action in self.actions}

        if random.uniform(0, 1) < self.epsilon:
            # Exploration: Avoid opposite direction
            possible_actions = self.actions[:]
            if self.snake.direction == 'up':
                possible_actions.remove('down')
            elif self.snake.direction == 'down':
                possible_actions.remove('up')
            elif self.snake.direction == 'left':
                possible_actions.remove('right')
            elif self.snake.direction == 'right':
                possible_actions.remove('left')

            return random.choice(possible_actions)
        else:
            # Exploitation: Choose the best action based on Q-values
            return self.get_best_action(state)

    def get_best_action(self, state):
        # Return the action with the highest Q-value for the given state
        return max(self.q_values[state], key=self.q_values[state].get)

    def update_q_value(self, state, action, reward, next_state):
        # Initialize next_state if it does not exist in q_values
        if next_state not in self.q_values:
            self.q_values[next_state] = {action: 0 for action in self.actions}

        max_next_q = max(self.q_values[next_state].values())
        current_q = self.q_values[state][action]
        self.q_values[state][action] = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)

    def show_episode_progress(self, episode, total_episodes, iteration, total_iterations):
        """Function to display the episode and iteration progress on the screen"""
        font = pygame.font.SysFont('Arial', 24)  # Set font and size
        progress_text = f"Episode {episode}/{total_episodes}, Iteration {iteration}/{total_iterations}"
        text_surface = font.render(progress_text, True, (255, 255, 255))  # White text
        self.screen.blit(text_surface, (10, 10))  # Position the text at top-left of the screen
        pygame.display.update()  # Update the display with new text

    def train(self, num_episodes, num_iterations_per_episode):
        for episode in range(1, num_episodes + 1):
            game_over = False
            self.snake.reset()
            self.food.relocate()

            for iteration in range(1, num_iterations_per_episode + 1):
                if game_over:
                    break
                
                # Show the progress every iteration
                self.show_episode_progress(episode, num_episodes, iteration, num_iterations_per_episode)
                
                # Get the current state and choose an action
                state = self.get_state()
                action = self.choose_action(state)
                self.snake.change_direction(action)
                self.snake.move()

                # Check for collisions and update rewards
                head = self.snake.body[0]
                reward = 0
                if head == self.food.position:
                    reward = 10
                    self.food.relocate()
                elif head in self.snake.body[1:] or head[0] < PLAYABLE_X_OFFSET or head[0] >= PLAYABLE_X_OFFSET + PLAYABLE_WIDTH or head[1] < PLAYABLE_Y_OFFSET or head[1] >= PLAYABLE_Y_OFFSET + PLAYABLE_HEIGHT:
                    reward = -100
                    game_over = True

                # Update the Q-value
                next_state = self.get_state()
                self.update_q_value(state, action, reward, next_state)

            # Optionally decay epsilon over time to reduce exploration
            self.epsilon = max(0.1, self.epsilon * 0.99)  # Decaying epsilon after each episode
