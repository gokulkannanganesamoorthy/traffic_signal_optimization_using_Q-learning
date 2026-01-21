import os
import traci
import numpy as np
import pickle
from environment import TrafficEnv
from agent import QLearningAgent

import argparse

# SUMO configuration
CONFIG_PATH = "simulation/sumo_config.sumocfg"
MAX_STEPS = 1000

def load_q_table(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def run_evaluation(gui=False):
    if not os.path.exists("models/q_table.pkl"):
        print("No model found. Run training first.")
        return
    
    sumo_binary = "sumo-gui" if gui else "sumo"
    env = TrafficEnv(sumo_binary, CONFIG_PATH, MAX_STEPS)
    
    # Initialize agent with loaded Q-table
    agent = QLearningAgent(action_space_size=env.action_space.n, state_space_size=None, epsilon=0.0)
    agent.q_table = load_q_table("models/q_table.pkl")
    
    print(f"Starting evaluation (Mode: {sumo_binary})...")
    state = env.reset()
    total_reward = 0
    done = False
    
    while not done:
        # Choose action greedily (epsilon=0)
        action = agent.choose_action(state)
        next_state, reward, done, _ = env.step(action)
        
        state = next_state
        total_reward += reward
        
    print(f"Evaluation Total Reward: {total_reward}")
    env.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gui", action="store_true", help="Run with SUMO GUI")
    args = parser.parse_args()
    
    run_evaluation(args.gui)
