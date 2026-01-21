# Traffic Signal Optimization using Q-Learning

An Reinforcement Learning (RL) project to optimize traffic signal timings in a SUMO simulation environment.

## Project Structure

- `simulation/`: SUMO configuration and network files.
- `src/`: Python source code.
  - `agent.py`: Q-Learning agent implementation.
  - `train.py`: Main training loop.
  - `generator.py`: Traffic demand generator.
- `models/`: Saved Q-table models.

## Setup

1. **Install Dependencies**:

   ```bash
   brew install sumo
   pip install -r requirements.txt
   ```

2. **Generate Network**:
   (The network files are generated automatically or provided in `simulation/`)

   ```bash
   netconvert --node-files simulation/nodes.xml --edge-files simulation/edges.xml --output-file simulation/network.net.xml
   ```

3. **Run Training**:
   ```bash
   python src/train.py
   ```

## Algorithm

Uses Q-Learning with state representation based on queue lengths and actions controlling phase switches.
