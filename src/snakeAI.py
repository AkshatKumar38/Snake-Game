import random
import math, matplotlib.pyplot as plt
from settings import *
class SnakeAI:
    def __init__(self, snake, food, actions):
        self.snake = snake
        self.food = food
        self.actions = actions
        self.q_values = {}
        self.epsilon = 0.8  # Initial exploration rate
        self.alpha = 0.9    # Learning rate
        self.gamma = 0.95   # Discount factor
        self.epsilon_min = 0.1  # Minimum epsilon
        self.epsilon_decay = 0.99  # Decay rate for epsilon

    def get_state(self):
        head = self.snake.body[0]
        food = self.food.position

        # Relative position of food
        food_dir_x = 1 if food[0] > head[0] else -1 if food[0] < head[0] else 0
        food_dir_y = 1 if food[1] > head[1] else -1 if food[1] < head[1] else 0

        # Obstacle indicators
        left_obstacle = self.is_obstacle(head, self.snake.direction, "LEFT")
        right_obstacle = self.is_obstacle(head, self.snake.direction, "RIGHT")
        front_obstacle = self.is_obstacle(head, self.snake.direction, "FORWARD")

        return (food_dir_x, food_dir_y, left_obstacle, right_obstacle, front_obstacle)
    def is_obstacle(self, head, direction, relative_dir):
        # Determine next position based on direction and relative direction
        dx, dy = 0, 0
        if direction == "UP":
            dx, dy = (-1, 0) if relative_dir == "LEFT" else (1, 0) if relative_dir == "RIGHT" else (0, -1)
        elif direction == "DOWN":
            dx, dy = (1, 0) if relative_dir == "LEFT" else (-1, 0) if relative_dir == "RIGHT" else (0, 1)
        elif direction == "LEFT":
            dx, dy = (0, 1) if relative_dir == "LEFT" else (0, -1) if relative_dir == "RIGHT" else (-1, 0)
        elif direction == "RIGHT":
            dx, dy = (0, -1) if relative_dir == "LEFT" else (0, 1) if relative_dir == "RIGHT" else (1, 0)

        next_pos = (head[0] + dx, head[1] + dy)

        # Check for collisions with walls or snake body
        return (
            next_pos in self.snake.body
            or next_pos[0] < PLAYABLE_X_OFFSET
            or next_pos[0] >= PLAYABLE_X_OFFSET + PLAYABLE_WIDTH
            or next_pos[1] < PLAYABLE_Y_OFFSET
            or next_pos[1] >= PLAYABLE_Y_OFFSET + PLAYABLE_HEIGHT
        )

    def choose_action(self, state):
        # Initialize Q-values for a new state
        if state not in self.q_values:
            self.q_values[state] = {action: 0 for action in self.actions}

        if random.uniform(0, 1) < self.epsilon:
            # Exploration: Avoid invalid actions (opposite to current direction)
            valid_actions = self.actions[:]
            if self.snake.direction == "UP":
                valid_actions.remove("DOWN")
            elif self.snake.direction == "DOWN":
                valid_actions.remove("UP")
            elif self.snake.direction == "LEFT":
                valid_actions.remove("RIGHT")
            elif self.snake.direction == "RIGHT":
                valid_actions.remove("LEFT")
            return random.choice(valid_actions)
        else:
            # Exploitation: Choose the best action based on Q-values
            return self.get_best_action(state)

    def get_best_action(self, state):
        return max(self.q_values[state], key=self.q_values[state].get)

    def update_q_value(self, state, action, reward, next_state):
        if next_state not in self.q_values:
            self.q_values[next_state] = {action: 0 for action in self.actions}

        max_next_q = max(self.q_values[next_state].values())
        current_q = self.q_values[state][action]
        self.q_values[state][action] = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)

    def train(self, num_episodes):
        rewards_history = []  # To track rewards for analysis
        for episode in range(num_episodes):
            game_over = False
            self.snake.__init__()  # Reset snake for a new episode
            self.food.relocate()  # Relocate food for a new episode
            total_reward = 0  # Track cumulative reward

            while not game_over and num_episodes > 0:
                state = self.get_state()
                action = self.choose_action(state)
                self.snake.change_direction(action)
                self.snake.move()

                head = self.snake.body[0]
                reward = 0

                if head == self.food.position:
                    reward = 50  # Reward for eating food
                    self.snake.eat_food()
                    self.food.relocate()
                elif head in self.snake.body[1:] or head[0] < PLAYABLE_X_OFFSET or head[0] >= PLAYABLE_X_OFFSET + PLAYABLE_WIDTH or head[1] < PLAYABLE_Y_OFFSET or head[1] >= PLAYABLE_Y_OFFSET + PLAYABLE_HEIGHT:
                    reward = -100  # Penalty for collision
                    game_over = True
                else:
                    # Encourage moving closer to food
                    old_distance = math.sqrt((head[0] - self.food.position[0])**2 + (head[1] - self.food.position[1])**2)
                    new_distance = math.sqrt((self.snake.body[0][0] - self.food.position[0])**2 + (self.snake.body[0][1] - self.food.position[1])**2)
                    distance_reward = 10 * (old_distance - new_distance)  # Positive for getting closer, negative for moving away
                    reward = max(-1, distance_reward)
                    # Penalize wasting time
                    
                total_reward += reward
                if total_reward < -100:
                    break
                # Update AI Q-values
                next_state = self.get_state()
                self.update_q_value(state, action, reward, next_state)

            rewards_history.append(total_reward)
            # Decay epsilon after each episode
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

            # Output progress
            if (episode + 1) % 100 == 0:
                print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}, Epsilon: {self.epsilon:.2f}")
        # Plot rewards after training
        plt.plot(rewards_history)
        plt.title("Training Rewards Over Episodes")
        plt.xlabel("Episode")
        plt.ylabel("Total Reward")
        plt.show()