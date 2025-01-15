import numpy as np
import random
import pickle

class SnakeAI:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995, min_exploration_rate=0.01):

        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        
        # Initialize the Q-table
        self.q_table = {}

    def encode_state(self, snake, food):

        head = snake.body[0]
        food_position = food.position
        # Example encoding: relative position of food and obstacles
        return (head[0] - food_position[0], head[1] - food_position[1])

    def get_q_value(self, state, action):
        """Get Q-value for a specific state-action pair."""
        return self.q_table.get((state, action), 0.0)
    
    def choose_action(self, state):
        """
        Choose an action using the epsilon-greedy policy.
        :param state: Current state of the environment.
        :return: Action to take.
        """
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(range(self.action_size))  # Explore: random action
        else:
            # Exploit: choose the action with the highest Q-value
            q_values = [self.get_q_value(state, a) for a in range(self.action_size)]
            return np.argmax(q_values)
    
    def update_q_table(self, state, action, reward, next_state, done):
        """
        Update the Q-table using the Q-learning algorithm.
        :param state: Current state.
        :param action: Action taken.
        :param reward: Reward received.
        :param next_state: Next state after taking the action.
        :param done: Whether the episode is done.
        """
        max_future_q = max([self.get_q_value(next_state, a) for a in range(self.action_size)]) if not done else 0
        current_q = self.get_q_value(state, action)
        new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (reward + self.discount_factor * max_future_q)
        self.q_table[(state, action)] = new_q
    
    def decay_exploration_rate(self):
        """Decay the exploration rate after each episode."""
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
    
    def save_q_table(self, filename):
        """Save the Q-table to a file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
    
    def load_q_table(self, filename):
        """Load the Q-table from a file."""
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
