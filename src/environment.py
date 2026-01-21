import traci
import gym
import os
import numpy as np
from generator import generate_route_file

class TrafficEnv(gym.Env):
    def __init__(self, sumo_binary, config_path, max_steps=1000):
        self.sumo_binary = sumo_binary
        self.config_path = config_path
        self.max_steps = max_steps
        self.step_count = 0
        
        # Check SUMO_HOME
        if 'SUMO_HOME' not in os.environ:
             # Try to guess
             try:
                 import sumolib
                 # logic to find home?
                 pass 
             except ImportError:
                 pass
        
        # Action space: 0 = Keep/Set NS Green, 1 = Keep/Set EW Green
        self.action_space = gym.spaces.Discrete(2)
        
        # State space: Queue lengths (discrete) + Current Phase
        # 8 lanes * 3 discrete levels + 1 phase (approx)
        # For simplicity, we define box/tuple space or just return raw state
        self.observation_space = gym.spaces.Box(low=0, high=100, shape=(9,), dtype=np.int32)
        
        self.lanes = ["n_to_c_0", "n_to_c_1", "s_to_c_0", "s_to_c_1", 
                      "e_to_c_0", "e_to_c_1", "w_to_c_0", "w_to_c_1"]
        self.label = "sim"
        self.run_id = 0

    def reset(self):
        self.run_id += 1
        # Generate flows
        generate_route_file("simulation/routes.rou.xml", self.max_steps, n_cars=800)
        
        try:
            traci.close()
        except:
            pass
            
        traci.start([self.sumo_binary, "-c", self.config_path], label=self.label)
        self.step_count = 0
        return self._get_state()

    def step(self, action):
        self.step_count += 1
        
        # Action Logic
        current_phase = traci.trafficlight.getPhase("c")
        
        # Action 0: NS Green
        # Action 1: EW Green
        
        # If we want to change, we must go through yellow.
        # Simple Logic:
        # If Action wants NS and we are EW -> Set Yellow (transition to NS)
        # If Action wants EW and we are NS -> Set Yellow (transition to EW)
        
        if action == 0 and current_phase == 2: # Want NS, currently EW
             traci.trafficlight.setPhase("c", 3) # Yellow EW
        elif action == 1 and current_phase == 0: # Want EW, currently NS
             traci.trafficlight.setPhase("c", 1) # Yellow NS
             
        traci.simulationStep()
        
        state = self._get_state()
        reward = self._get_reward()
        done = self.step_count >= self.max_steps
        
        return state, reward, done, {}

    def _get_state(self):
        state = []
        for lane in self.lanes:
            q_len = traci.lane.getLastStepHaltingNumber(lane)
            # Discretize
            if q_len < 3: state.append(0)
            elif q_len < 8: state.append(1)
            else: state.append(2)
            
        phase = traci.trafficlight.getPhase("c")
        state.append(phase)
        return tuple(state)

    def _get_reward(self):
        total_waiting = 0
        for lane in self.lanes:
            total_waiting += traci.lane.getLastStepHaltingNumber(lane)
        return -total_waiting

    def close(self):
        traci.close()
