import os
import sys
import traci
import numpy as np
import time
from agent import QLearningAgent
from environment import TrafficEnv

# SUMO configuration
SUMO_BINARY = "sumo" # or "sumo-gui"
CONFIG_PATH = "simulation/sumo_config.sumocfg"

# Training parameters
EPISODES = 100
MAX_STEPS = 1000
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.4 # Higher initial exploration
MIN_EPSILON = 0.01
DECAY = 0.99 

def run():
    env = TrafficEnv(SUMO_BINARY, CONFIG_PATH, MAX_STEPS)
    
    agent = QLearningAgent(action_space_size=env.action_space.n, 
                           state_space_size=None, 
                           alpha=ALPHA, gamma=GAMMA, epsilon=EPSILON)
    
    episode_rewards = []
    
    for episode in range(EPISODES):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            
            agent.learn(state, action, reward, next_state)
            
            state = next_state
            total_reward += reward
        
        episode_rewards.append(total_reward)

        # Decay Epsilon
        if agent.epsilon > MIN_EPSILON:
            agent.epsilon *= DECAY
            
        print(f"Episode {episode + 1}: Total Reward: {total_reward}, Epsilon: {agent.epsilon:.4f}")
        
    agent.save_model("models/q_table.pkl")
    env.close()
    
    # Plotting
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    plt.plot(episode_rewards)
    plt.title("Total Reward per Episode")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.savefig("reward_plot.png")
    print("Plot saved to reward_plot.png")

if __name__ == "__main__":
    # Ensure models dir exists
    if not os.path.exists("models"):
        os.makedirs("models")
        
    run()
