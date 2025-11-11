# Conway's Game of Life

A Python implementation of Conway's Game of Life, a cellular automaton devised by mathematician John Conway. This enhanced version includes **mutations** and a **character creation system** to customize cells.

## About

The Game of Life is a zero-player game where the evolution is determined by its initial state. The universe is an infinite grid of square cells, each of which is in one of two possible states: alive or dead.

### Rules

1. Any live cell with 2 or 3 live neighbors survives to the next generation
2. Any dead cell with exactly 3 live neighbors becomes a live cell
3. All other live cells die in the next generation (underpopulation or overpopulation)
4. All other dead cells stay dead

## New Features

### Mutations

Add randomness to the simulation with mutations! When enabled, cells can:
- Spontaneously die or come to life
- Change their visual properties (color, symbol)

Configure mutation rate from 0.0 (no mutations) to 1.0 (maximum chaos) when starting the simulation.

### Character Creation System

Customize your cells with unique properties:
- **Name**: Give your cell types meaningful names
- **Symbol**: Choose from various symbols (█, ●, ■, ◆, ★)
- **Color**: Assign colors to differentiate cell types

New cells inherit properties from their neighbors, creating evolving populations with diverse characteristics!

## Usage

### Running the Simulation

```bash
python3 game_of_life.py
```

The program will prompt you to:
1. Select from classic patterns or create custom cells:
   - **Glider**: A pattern that moves across the grid
   - **Blinker**: A simple oscillator that alternates between two states
   - **Toad**: Another oscillator with a period of 2
   - **Beacon**: A period-2 oscillator
   - **Pulsar**: A period-3 oscillator
   - **Custom cells**: Create your own cell types with unique characteristics

2. Set a mutation rate (0.0 to 1.0)

3. If using custom cells, design your cell types with:
   - Custom names
   - Unique symbols
   - Different colors

Press `Ctrl+C` to stop the simulation.

### Running Tests

```bash
python3 -m unittest test_game_of_life -v
```

## Implementation

The implementation includes:
- `Cell` class for customizable cells with properties
- `GameOfLife` class with core game logic
- Mutation system for random changes
- Character creation system for cell customization
- Several predefined patterns (glider, blinker, toad, beacon, pulsar)
- Terminal-based visualization with custom symbols
- Comprehensive unit tests (23 tests covering all features)

## Requirements

- Python 3.6 or higher
- No external dependencies required
