import numpy as np
import random

class QLearningAgent:
    def __init__(self, action_space_size, state_space_size, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.action_space_size = action_space_size
        self.q_table = {} # Dictionary for Q-table to handle sparse states or large tables

    def get_state_key(self, state):
        """Convert state list/tuple to a string or tuple key for dictionary."""
        return tuple(state)

    def choose_action(self, state):
        state_key = self.get_state_key(state)
        
        # Exploration
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.action_space_size - 1)
        
        # Exploitation
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_space_size)
            
        return np.argmax(self.q_table[state_key])

    def learn(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_space_size)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(self.action_space_size)

        old_value = self.q_table[state_key][action]
        next_max = np.max(self.q_table[next_state_key])
        
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state_key][action] = new_value

    def save_model(self, path):
        import pickle
        with open(path, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_model(self, path):
        import pickle
        with open(path, 'rb') as f:
            self.q_table = pickle.load(f)
