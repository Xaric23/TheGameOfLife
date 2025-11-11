# Conway's Game of Life

A Python implementation of Conway's Game of Life, a cellular automaton devised by mathematician John Conway.

## About

The Game of Life is a zero-player game where the evolution is determined by its initial state. The universe is an infinite grid of square cells, each of which is in one of two possible states: alive or dead.

### Rules

1. Any live cell with 2 or 3 live neighbors survives to the next generation
2. Any dead cell with exactly 3 live neighbors becomes a live cell
3. All other live cells die in the next generation (underpopulation or overpopulation)
4. All other dead cells stay dead

## Usage

### Running the Simulation

```bash
python3 game_of_life.py
```

The program will prompt you to select from several classic patterns:
- **Glider**: A pattern that moves across the grid
- **Blinker**: A simple oscillator that alternates between two states
- **Toad**: Another oscillator with a period of 2
- **Beacon**: A period-2 oscillator
- **Pulsar**: A period-3 oscillator

Press `Ctrl+C` to stop the simulation.

### Running Tests

```bash
python3 -m unittest test_game_of_life -v
```

## Implementation

The implementation includes:
- `GameOfLife` class with core game logic
- Several predefined patterns (glider, blinker, toad, beacon, pulsar)
- Terminal-based visualization
- Comprehensive unit tests

## Requirements

- Python 3.6 or higher
- No external dependencies required
