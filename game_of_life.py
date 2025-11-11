"""
Conway's Game of Life Implementation

Rules:
1. Any live cell with 2 or 3 live neighbors survives
2. Any dead cell with exactly 3 live neighbors becomes a live cell
3. All other live cells die in the next generation
4. All other dead cells stay dead
"""

import time
import sys
import os


class GameOfLife:
    """Conway's Game of Life simulator"""
    
    def __init__(self, width=40, height=20):
        """
        Initialize the Game of Life grid
        
        Args:
            width: Width of the grid
            height: Height of the grid
        """
        self.width = width
        self.height = height
        self.grid = [[False for _ in range(width)] for _ in range(height)]
        self.generation = 0
    
    def set_cell(self, x, y, alive=True):
        """Set a cell to alive or dead"""
        if 0 <= x < self.height and 0 <= y < self.width:
            self.grid[x][y] = alive
    
    def get_cell(self, x, y):
        """Get the state of a cell"""
        if 0 <= x < self.height and 0 <= y < self.width:
            return self.grid[x][y]
        return False
    
    def count_neighbors(self, x, y):
        """Count the number of alive neighbors for a cell"""
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.height and 0 <= ny < self.width:
                    if self.grid[nx][ny]:
                        count += 1
        return count
    
    def next_generation(self):
        """Compute the next generation based on Game of Life rules"""
        new_grid = [[False for _ in range(self.width)] for _ in range(self.height)]
        
        for x in range(self.height):
            for y in range(self.width):
                neighbors = self.count_neighbors(x, y)
                alive = self.grid[x][y]
                
                # Apply Game of Life rules
                if alive:
                    # Live cell with 2 or 3 neighbors survives
                    if neighbors == 2 or neighbors == 3:
                        new_grid[x][y] = True
                else:
                    # Dead cell with exactly 3 neighbors becomes alive
                    if neighbors == 3:
                        new_grid[x][y] = True
        
        self.grid = new_grid
        self.generation += 1
    
    def clear_grid(self):
        """Clear all cells"""
        self.grid = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.generation = 0
    
    def load_pattern(self, pattern_name):
        """Load a predefined pattern"""
        self.clear_grid()
        
        patterns = {
            'glider': [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)],
            'blinker': [(1, 1), (1, 2), (1, 3)],
            'toad': [(2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3)],
            'beacon': [(1, 1), (1, 2), (2, 1), (3, 4), (4, 3), (4, 4)],
            'pulsar': [
                (2, 4), (2, 5), (2, 6), (2, 10), (2, 11), (2, 12),
                (4, 2), (4, 7), (4, 9), (4, 14),
                (5, 2), (5, 7), (5, 9), (5, 14),
                (6, 2), (6, 7), (6, 9), (6, 14),
                (7, 4), (7, 5), (7, 6), (7, 10), (7, 11), (7, 12),
                (9, 4), (9, 5), (9, 6), (9, 10), (9, 11), (9, 12),
                (10, 2), (10, 7), (10, 9), (10, 14),
                (11, 2), (11, 7), (11, 9), (11, 14),
                (12, 2), (12, 7), (12, 9), (12, 14),
                (14, 4), (14, 5), (14, 6), (14, 10), (14, 11), (14, 12)
            ]
        }
        
        if pattern_name in patterns:
            for x, y in patterns[pattern_name]:
                self.set_cell(x, y, True)
            return True
        return False
    
    def display(self):
        """Display the current grid state"""
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"Generation: {self.generation}")
        print("=" * (self.width + 2))
        
        for row in self.grid:
            print("|" + "".join("█" if cell else " " for cell in row) + "|")
        
        print("=" * (self.width + 2))
    
    def __str__(self):
        """String representation of the grid"""
        result = f"Generation: {self.generation}\n"
        for row in self.grid:
            result += "".join("█" if cell else "." for cell in row) + "\n"
        return result


def main():
    """Main function to run the Game of Life simulation"""
    print("Conway's Game of Life")
    print("=" * 40)
    print("\nAvailable patterns:")
    print("1. Glider")
    print("2. Blinker")
    print("3. Toad")
    print("4. Beacon")
    print("5. Pulsar")
    print("\nPress Ctrl+C to exit\n")
    
    # Get user choice
    choice = input("Select a pattern (1-5): ").strip()
    
    patterns = {
        '1': 'glider',
        '2': 'blinker',
        '3': 'toad',
        '4': 'beacon',
        '5': 'pulsar'
    }
    
    pattern = patterns.get(choice, 'glider')
    
    # Create game instance
    game = GameOfLife(width=50, height=25)
    game.load_pattern(pattern)
    
    try:
        # Run simulation
        while True:
            game.display()
            time.sleep(0.2)
            game.next_generation()
    except KeyboardInterrupt:
        print("\n\nSimulation ended.")
        print(f"Total generations: {game.generation}")


if __name__ == "__main__":
    main()
