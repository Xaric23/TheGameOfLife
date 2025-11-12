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
import random


class Cell:
    """Represents a customizable cell in the Game of Life"""
    
    def __init__(self, alive=False, name="", color="white", symbol="█"):
        """
        Initialize a cell with custom properties
        
        Args:
            alive: Whether the cell is alive
            name: Custom name for the cell
            color: Color for the cell (default: white)
            symbol: Symbol to display for the cell (default: █)
        """
        self.alive = alive
        self.name = name
        self.color = color
        self.symbol = symbol
    
    def __bool__(self):
        """Allow cell to be used in boolean context"""
        return self.alive
    
    def copy(self):
        """Create a copy of this cell"""
        return Cell(self.alive, self.name, self.color, self.symbol)


class GameOfLife:
    """Conway's Game of Life simulator"""
    
    def __init__(self, width=40, height=20, mutation_rate=0.0):
        """
        Initialize the Game of Life grid
        
        Args:
            width: Width of the grid
            height: Height of the grid
            mutation_rate: Probability of random mutation (0.0 to 1.0)
        """
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.generation = 0
        self.mutation_rate = mutation_rate
        self.cell_types = []  # Store custom cell types
    
    def set_cell(self, x, y, alive=True, cell_type=None):
        """
        Set a cell to alive or dead
        
        Args:
            x: Row position
            y: Column position
            alive: Whether the cell should be alive
            cell_type: Optional Cell object with custom properties
        """
        if 0 <= x < self.height and 0 <= y < self.width:
            if cell_type is not None:
                self.grid[x][y] = cell_type.copy()
            else:
                self.grid[x][y].alive = alive
    
    def get_cell(self, x, y):
        """Get the state of a cell"""
        if 0 <= x < self.height and 0 <= y < self.width:
            return self.grid[x][y].alive
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
                    if self.grid[nx][ny].alive:
                        count += 1
        return count
    
    def next_generation(self):
        """Compute the next generation based on Game of Life rules"""
        new_grid = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        
        for x in range(self.height):
            for y in range(self.width):
                neighbors = self.count_neighbors(x, y)
                alive = self.grid[x][y].alive
                
                # Apply Game of Life rules
                if alive:
                    # Live cell with 2 or 3 neighbors survives
                    if neighbors == 2 or neighbors == 3:
                        new_grid[x][y] = self.grid[x][y].copy()
                else:
                    # Dead cell with exactly 3 neighbors becomes alive
                    if neighbors == 3:
                        # Create offspring from two compatible parent cells
                        alive_neighbors = self._get_alive_neighbors(x, y)
                        parent1, parent2 = self._select_parents(alive_neighbors)
                        if parent1:
                            new_grid[x][y] = self._create_offspring(parent1, parent2)
                        else:
                            # Fallback if no parents available
                            new_grid[x][y].alive = True
                
                # Apply mutations
                if self.mutation_rate > 0 and random.random() < self.mutation_rate:
                    if new_grid[x][y].alive:
                        # Mutate living cell - mostly change properties, rarely kill it
                        if random.random() < 0.03:  # Only 3% chance to die from mutation
                            new_grid[x][y].alive = False
                        else:
                            self._mutate_cell(new_grid[x][y])
                    else:
                        # Very rarely birth a cell through mutation
                        if random.random() < 0.01:  # Only 1% chance to spontaneously birth
                            new_grid[x][y].alive = True
                            self._mutate_cell(new_grid[x][y])
        
        self.grid = new_grid
        self.generation += 1
    
    def _get_random_neighbor_cell(self, x, y):
        """Get a random alive neighbor cell"""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.height and 0 <= ny < self.width:
                    if self.grid[nx][ny].alive:
                        neighbors.append(self.grid[nx][ny])
        
        if neighbors:
            return random.choice(neighbors)
        return Cell(alive=True)
    
    def _get_alive_neighbors(self, x, y):
        """Get list of all alive neighbor cells"""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.height and 0 <= ny < self.width:
                    if self.grid[nx][ny].alive:
                        neighbors.append(self.grid[nx][ny])
        return neighbors
    
    def _are_compatible(self, cell1, cell2):
        """
        Check if two cells are compatible for producing offspring
        
        Cells are compatible if:
        - They have different symbols OR different colors (promoting diversity)
        - OR both have custom names (indicating they are custom cell types)
        """
        # If both have custom names, they're compatible
        if cell1.name and cell2.name:
            return True
        
        # If they differ in appearance, they're compatible
        if cell1.symbol != cell2.symbol or cell1.color != cell2.color:
            return True
        
        return False
    
    def _select_parents(self, neighbors):
        """
        Select 2 compatible parent cells from the list of neighbors
        
        Args:
            neighbors: List of alive neighbor cells
            
        Returns:
            Tuple of (parent1, parent2) or (parent, None) if only one parent available
        """
        if len(neighbors) < 2:
            return (neighbors[0] if neighbors else None, None)
        
        # Try to find compatible parents
        random.shuffle(neighbors)
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if self._are_compatible(neighbors[i], neighbors[j]):
                    return (neighbors[i], neighbors[j])
        
        # If no compatible pair found, use first two neighbors
        return (neighbors[0], neighbors[1])
    
    def _create_offspring(self, parent1, parent2):
        """
        Create offspring cell from two parent cells
        
        The offspring inherits properties from both parents:
        - Symbol: randomly chosen from one parent
        - Color: randomly chosen from one parent
        - Name: blended from both parents if they have names
        
        Args:
            parent1: First parent cell
            parent2: Second parent cell (can be None)
            
        Returns:
            New Cell with blended properties
        """
        offspring = Cell(alive=True)
        
        if parent2 is None:
            # Single parent - just inherit properties
            offspring.symbol = parent1.symbol
            offspring.color = parent1.color
            offspring.name = parent1.name
        else:
            # Two parents - blend properties
            offspring.symbol = random.choice([parent1.symbol, parent2.symbol])
            offspring.color = random.choice([parent1.color, parent2.color])
            
            # Blend names if both parents have names
            if parent1.name and parent2.name:
                # Create hybrid name
                if random.random() < 0.5:
                    offspring.name = f"{parent1.name}-{parent2.name}"
                else:
                    offspring.name = f"{parent2.name}-{parent1.name}"
            elif parent1.name:
                offspring.name = parent1.name
            elif parent2.name:
                offspring.name = parent2.name
        
        return offspring
    
    def _mutate_cell(self, cell):
        """Apply random mutation to a cell's properties"""
        colors = ["white", "red", "green", "blue", "yellow", "magenta", "cyan"]
        symbols = ["█", "●", "■", "◆", "★", "♦", "▲"]
        
        if random.random() < 0.5:
            cell.color = random.choice(colors)
        if random.random() < 0.3:
            cell.symbol = random.choice(symbols)
    
    def add_cell_type(self, name, color="white", symbol="█"):
        """
        Add a custom cell type
        
        Args:
            name: Name of the cell type
            color: Color for this cell type
            symbol: Symbol to display for this cell type
        """
        cell_type = Cell(alive=True, name=name, color=color, symbol=symbol)
        self.cell_types.append(cell_type)
        return cell_type
    
    def clear_grid(self):
        """Clear all cells"""
        self.grid = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
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
        
        print(f"Generation: {self.generation} | Mutation Rate: {self.mutation_rate:.1%}")
        print("=" * (self.width + 2))
        
        for row in self.grid:
            print("|" + "".join(cell.symbol if cell.alive else " " for cell in row) + "|")
        
        print("=" * (self.width + 2))
    
    def __str__(self):
        """String representation of the grid"""
        result = f"Generation: {self.generation}\n"
        for row in self.grid:
            result += "".join(cell.symbol if cell.alive else "." for cell in row) + "\n"
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
    print("6. Custom cells with character creation")
    print("\nPress Ctrl+C to exit\n")
    
    # Get user choice
    choice = input("Select a pattern (1-6): ").strip()
    
    # Get mutation rate
    mutation_input = input("Enter mutation rate (0.0-1.0, default 0.0): ").strip()
    try:
        mutation_rate = float(mutation_input) if mutation_input else 0.0
        mutation_rate = max(0.0, min(1.0, mutation_rate))
    except ValueError:
        mutation_rate = 0.0
    
    patterns = {
        '1': 'glider',
        '2': 'blinker',
        '3': 'toad',
        '4': 'beacon',
        '5': 'pulsar'
    }
    
    # Create game instance
    game = GameOfLife(width=50, height=25, mutation_rate=mutation_rate)
    
    if choice == '6':
        # Character creation mode
        print("\n--- Character Creation ---")
        num_types = input("How many custom cell types? (1-5): ").strip()
        try:
            num_types = max(1, min(5, int(num_types)))
        except ValueError:
            num_types = 1
        
        symbols = ["█", "●", "■", "◆", "★"]
        colors = ["white", "red", "green", "blue", "yellow"]
        
        for i in range(num_types):
            print(f"\nCell Type {i + 1}:")
            name = input(f"  Name (default: Cell{i+1}): ").strip() or f"Cell{i+1}"
            
            print("  Available symbols: 1=█ 2=● 3=■ 4=◆ 5=★")
            symbol_choice = input(f"  Symbol (1-5, default: {i+1}): ").strip()
            try:
                symbol = symbols[int(symbol_choice) - 1]
            except (ValueError, IndexError):
                symbol = symbols[i % len(symbols)]
            
            print("  Available colors: 1=white 2=red 3=green 4=blue 5=yellow")
            color_choice = input(f"  Color (1-5, default: {i+1}): ").strip()
            try:
                color = colors[int(color_choice) - 1]
            except (ValueError, IndexError):
                color = colors[i % len(colors)]
            
            cell_type = game.add_cell_type(name, color, symbol)
            print(f"  Created: {name} ({symbol})")
        
        # Place custom cells in a pattern
        print("\nCreating pattern with custom cells...")
        # Create a simple glider-like pattern with custom cells
        if game.cell_types:
            for i, (x, y) in enumerate([(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)]):
                cell_type = game.cell_types[i % len(game.cell_types)]
                game.set_cell(x, y, alive=True, cell_type=cell_type)
    else:
        pattern = patterns.get(choice, 'glider')
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
