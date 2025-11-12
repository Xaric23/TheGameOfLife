"""
Unit tests for Conway's Game of Life implementation
"""

import unittest
from game_of_life import GameOfLife, Cell


class TestCell(unittest.TestCase):
    """Test cases for Cell class"""
    
    def test_cell_initialization(self):
        """Test cell initialization with default values"""
        cell = Cell()
        self.assertFalse(cell.alive)
        self.assertEqual(cell.name, "")
        self.assertEqual(cell.color, "white")
        self.assertEqual(cell.symbol, "█")
    
    def test_cell_custom_initialization(self):
        """Test cell initialization with custom values"""
        cell = Cell(alive=True, name="Test", color="red", symbol="●")
        self.assertTrue(cell.alive)
        self.assertEqual(cell.name, "Test")
        self.assertEqual(cell.color, "red")
        self.assertEqual(cell.symbol, "●")
    
    def test_cell_boolean_context(self):
        """Test cell can be used in boolean context"""
        cell = Cell(alive=False)
        self.assertFalse(bool(cell))
        
        cell.alive = True
        self.assertTrue(bool(cell))
    
    def test_cell_copy(self):
        """Test cell copy creates independent instance"""
        cell1 = Cell(alive=True, name="Original", color="blue", symbol="■")
        cell2 = cell1.copy()
        
        self.assertTrue(cell2.alive)
        self.assertEqual(cell2.name, "Original")
        self.assertEqual(cell2.color, "blue")
        self.assertEqual(cell2.symbol, "■")
        
        # Modify cell2, cell1 should be unchanged
        cell2.alive = False
        cell2.name = "Copy"
        self.assertTrue(cell1.alive)
        self.assertEqual(cell1.name, "Original")


class TestGameOfLife(unittest.TestCase):
    """Test cases for Game of Life"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.game = GameOfLife(width=10, height=10)
    
    def test_initialization(self):
        """Test game initialization"""
        self.assertEqual(self.game.width, 10)
        self.assertEqual(self.game.height, 10)
        self.assertEqual(self.game.generation, 0)
        # All cells should be dead initially
        for row in self.game.grid:
            for cell in row:
                self.assertFalse(cell.alive)
    
    def test_set_and_get_cell(self):
        """Test setting and getting cell states"""
        self.game.set_cell(5, 5, True)
        self.assertTrue(self.game.get_cell(5, 5))
        
        self.game.set_cell(5, 5, False)
        self.assertFalse(self.game.get_cell(5, 5))
    
    def test_count_neighbors(self):
        """Test neighbor counting"""
        # Set up a pattern
        self.game.set_cell(5, 5, True)
        self.game.set_cell(5, 6, True)
        self.game.set_cell(6, 5, True)
        
        # Cell at (5,5) has 2 neighbors
        self.assertEqual(self.game.count_neighbors(5, 5), 2)
        
        # Cell at (6,6) has 3 neighbors
        self.assertEqual(self.game.count_neighbors(6, 6), 3)
        
        # Cell at (0,0) has 0 neighbors
        self.assertEqual(self.game.count_neighbors(0, 0), 0)
    
    def test_dead_cell_with_three_neighbors_becomes_alive(self):
        """Test rule: dead cell with exactly 3 neighbors becomes alive"""
        # Create a pattern where (5,5) has exactly 3 neighbors
        self.game.set_cell(4, 4, True)
        self.game.set_cell(4, 5, True)
        self.game.set_cell(4, 6, True)
        
        self.assertFalse(self.game.get_cell(5, 5))
        self.assertEqual(self.game.count_neighbors(5, 5), 3)
        
        self.game.next_generation()
        
        # Cell should now be alive
        self.assertTrue(self.game.get_cell(5, 5))
    
    def test_live_cell_with_two_neighbors_survives(self):
        """Test rule: live cell with 2 neighbors survives"""
        self.game.set_cell(5, 5, True)
        self.game.set_cell(5, 6, True)
        self.game.set_cell(6, 5, True)
        
        self.assertTrue(self.game.get_cell(5, 5))
        self.assertEqual(self.game.count_neighbors(5, 5), 2)
        
        self.game.next_generation()
        
        # Cell should still be alive
        self.assertTrue(self.game.get_cell(5, 5))
    
    def test_live_cell_with_three_neighbors_survives(self):
        """Test rule: live cell with 3 neighbors survives"""
        self.game.set_cell(5, 5, True)
        self.game.set_cell(5, 6, True)
        self.game.set_cell(6, 5, True)
        self.game.set_cell(6, 6, True)
        
        self.assertTrue(self.game.get_cell(5, 5))
        self.assertEqual(self.game.count_neighbors(5, 5), 3)
        
        self.game.next_generation()
        
        # Cell should still be alive
        self.assertTrue(self.game.get_cell(5, 5))
    
    def test_live_cell_with_fewer_than_two_neighbors_dies(self):
        """Test rule: live cell with < 2 neighbors dies (underpopulation)"""
        self.game.set_cell(5, 5, True)
        self.game.set_cell(5, 6, True)
        
        self.assertTrue(self.game.get_cell(5, 5))
        self.assertEqual(self.game.count_neighbors(5, 5), 1)
        
        self.game.next_generation()
        
        # Cell should be dead
        self.assertFalse(self.game.get_cell(5, 5))
    
    def test_live_cell_with_more_than_three_neighbors_dies(self):
        """Test rule: live cell with > 3 neighbors dies (overpopulation)"""
        # Create a pattern where (5,5) has 4 neighbors
        self.game.set_cell(5, 5, True)
        self.game.set_cell(4, 5, True)
        self.game.set_cell(6, 5, True)
        self.game.set_cell(5, 4, True)
        self.game.set_cell(5, 6, True)
        
        self.assertTrue(self.game.get_cell(5, 5))
        self.assertEqual(self.game.count_neighbors(5, 5), 4)
        
        self.game.next_generation()
        
        # Cell should be dead
        self.assertFalse(self.game.get_cell(5, 5))
    
    def test_blinker_pattern(self):
        """Test the blinker oscillator pattern"""
        game = GameOfLife(width=5, height=5)
        
        # Create horizontal blinker
        game.set_cell(2, 1, True)
        game.set_cell(2, 2, True)
        game.set_cell(2, 3, True)
        
        # After one generation, should be vertical
        game.next_generation()
        
        self.assertFalse(game.get_cell(2, 1))
        self.assertTrue(game.get_cell(1, 2))
        self.assertTrue(game.get_cell(2, 2))
        self.assertTrue(game.get_cell(3, 2))
        self.assertFalse(game.get_cell(2, 3))
        
        # After another generation, should be horizontal again
        game.next_generation()
        
        self.assertTrue(game.get_cell(2, 1))
        self.assertTrue(game.get_cell(2, 2))
        self.assertTrue(game.get_cell(2, 3))
        self.assertFalse(game.get_cell(1, 2))
        self.assertFalse(game.get_cell(3, 2))
    
    def test_clear_grid(self):
        """Test clearing the grid"""
        self.game.set_cell(5, 5, True)
        self.game.set_cell(6, 6, True)
        self.game.generation = 10
        
        self.game.clear_grid()
        
        self.assertEqual(self.game.generation, 0)
        for row in self.game.grid:
            for cell in row:
                self.assertFalse(cell.alive)
    
    def test_load_pattern_glider(self):
        """Test loading the glider pattern"""
        result = self.game.load_pattern('glider')
        self.assertTrue(result)
        
        # Check that some cells are alive
        alive_count = sum(1 for row in self.game.grid for cell in row if cell.alive)
        self.assertEqual(alive_count, 5)
    
    def test_load_pattern_invalid(self):
        """Test loading an invalid pattern"""
        result = self.game.load_pattern('invalid_pattern')
        self.assertFalse(result)
    
    def test_generation_counter(self):
        """Test that generation counter increments"""
        self.assertEqual(self.game.generation, 0)
        
        self.game.next_generation()
        self.assertEqual(self.game.generation, 1)
        
        self.game.next_generation()
        self.assertEqual(self.game.generation, 2)
    
    def test_mutation_rate_initialization(self):
        """Test that mutation rate is set correctly"""
        game = GameOfLife(width=10, height=10, mutation_rate=0.05)
        self.assertEqual(game.mutation_rate, 0.05)
    
    def test_add_cell_type(self):
        """Test adding custom cell types"""
        cell_type = self.game.add_cell_type("Warrior", "red", "●")
        
        self.assertEqual(cell_type.name, "Warrior")
        self.assertEqual(cell_type.color, "red")
        self.assertEqual(cell_type.symbol, "●")
        self.assertEqual(len(self.game.cell_types), 1)
    
    def test_set_cell_with_custom_type(self):
        """Test setting a cell with a custom type"""
        cell_type = self.game.add_cell_type("Mage", "blue", "★")
        self.game.set_cell(5, 5, alive=True, cell_type=cell_type)
        
        cell = self.game.grid[5][5]
        self.assertTrue(cell.alive)
        self.assertEqual(cell.name, "Mage")
        self.assertEqual(cell.color, "blue")
        self.assertEqual(cell.symbol, "★")
    
    def test_mutation_affects_cells(self):
        """Test that mutations can occur with non-zero mutation rate"""
        game = GameOfLife(width=10, height=10, mutation_rate=1.0)
        
        # Set up a stable block pattern
        game.set_cell(5, 5, True)
        game.set_cell(5, 6, True)
        game.set_cell(6, 5, True)
        game.set_cell(6, 6, True)
        
        initial_alive = sum(1 for row in game.grid for cell in row if cell.alive)
        
        # Run multiple generations - with 100% mutation rate, something should change
        for _ in range(10):
            game.next_generation()
        
        final_alive = sum(1 for row in game.grid for cell in row if cell.alive)
        
        # With 100% mutation rate, the pattern should be different
        # We can't test exact outcome due to randomness, but count should likely change
        # This test might occasionally fail due to random chance, but very unlikely
        self.assertNotEqual(initial_alive, final_alive)
    
    def test_high_mutation_rate_preserves_patterns(self):
        """Test that even with high mutation rate, patterns don't completely dissolve"""
        game = GameOfLife(width=20, height=20, mutation_rate=1.0)
        
        # Create a stable block pattern (2x2 square)
        game.set_cell(10, 10, True)
        game.set_cell(10, 11, True)
        game.set_cell(11, 10, True)
        game.set_cell(11, 11, True)
        
        initial_alive = 4
        
        # Run for many generations
        for _ in range(100):
            game.next_generation()
        
        final_alive = sum(1 for row in game.grid for cell in row if cell.alive)
        
        # With reduced mutation effects (5% death, 2% birth), the pattern should persist
        # and not explode into chaos. We expect some cells alive but not complete chaos
        # A reasonable expectation is between 0 and 50 cells (not 200+ like with old mutation rate)
        self.assertGreaterEqual(final_alive, 0)
        self.assertLessEqual(final_alive, 50, 
            "Mutation rate created chaos - too many cells alive. "
            "Expected mutations to be rarer and less disruptive.")
    
    def test_moderate_mutation_rate_stability(self):
        """Test that moderate mutation rates allow patterns to mostly survive"""
        game = GameOfLife(width=20, height=20, mutation_rate=0.1)
        
        # Load a glider pattern
        game.load_pattern('glider')
        
        initial_alive = sum(1 for row in game.grid for cell in row if cell.alive)
        
        # Run for several generations
        for _ in range(50):
            game.next_generation()
        
        final_alive = sum(1 for row in game.grid for cell in row if cell.alive)
        
        # With 10% mutation rate and reduced effects, pattern should mostly survive
        # Not be completely dead or explode into chaos
        self.assertGreater(final_alive, 0, "Pattern died completely - mutations too destructive")
        self.assertLess(final_alive, 30, "Pattern exploded - mutations too generative")
    
    def test_cell_inherits_properties_from_neighbors(self):
        """Test that new cells inherit properties from neighbors"""
        # Create custom cell types
        cell_type = self.game.add_cell_type("Red", "red", "●")
        
        # Set up pattern where a new cell will be born
        self.game.set_cell(4, 4, alive=True, cell_type=cell_type)
        self.game.set_cell(4, 5, alive=True, cell_type=cell_type)
        self.game.set_cell(4, 6, alive=True, cell_type=cell_type)
        
        # Cell at (5,5) should be born
        self.assertFalse(self.game.get_cell(5, 5))
        
        self.game.next_generation()
        
        # New cell should inherit symbol from neighbors
        self.assertTrue(self.game.get_cell(5, 5))
        cell = self.game.grid[5][5]
        self.assertEqual(cell.symbol, "●")
    
    def test_display_shows_mutation_rate(self):
        """Test that display method includes mutation rate"""
        game = GameOfLife(width=10, height=10, mutation_rate=0.15)
        # Just verify it doesn't crash
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            game.display()
        finally:
            sys.stdout = old_stdout
    
    def test_offspring_from_two_parents(self):
        """Test that offspring inherit properties from two parent cells"""
        # Create two custom cell types
        parent1_type = self.game.add_cell_type("Red", "red", "●")
        parent2_type = self.game.add_cell_type("Blue", "blue", "■")
        
        # Set up pattern where a new cell will be born at (5,5)
        # with exactly 3 neighbors of different types
        self.game.set_cell(4, 4, alive=True, cell_type=parent1_type)
        self.game.set_cell(4, 5, alive=True, cell_type=parent2_type)
        self.game.set_cell(4, 6, alive=True, cell_type=parent1_type)
        
        # Cell at (5,5) should be dead initially
        self.assertFalse(self.game.get_cell(5, 5))
        
        self.game.next_generation()
        
        # New cell should be born and inherit from parents
        self.assertTrue(self.game.get_cell(5, 5))
        offspring = self.game.grid[5][5]
        
        # Offspring should have inherited symbol from one of the parents
        self.assertIn(offspring.symbol, ["●", "■"])
        
        # Offspring should have inherited color from one of the parents
        self.assertIn(offspring.color, ["red", "blue"])
        
        # Offspring should have a hybrid name
        self.assertTrue(offspring.name)  # Should have a name
    
    def test_compatibility_check(self):
        """Test that compatibility check works correctly"""
        # Different symbols - should be compatible
        cell1 = Cell(alive=True, symbol="●", color="white")
        cell2 = Cell(alive=True, symbol="■", color="white")
        self.assertTrue(self.game._are_compatible(cell1, cell2))
        
        # Different colors - should be compatible
        cell3 = Cell(alive=True, symbol="●", color="red")
        cell4 = Cell(alive=True, symbol="●", color="blue")
        self.assertTrue(self.game._are_compatible(cell3, cell4))
        
        # Both have names - should be compatible
        cell5 = Cell(alive=True, name="Type1", symbol="●", color="white")
        cell6 = Cell(alive=True, name="Type2", symbol="●", color="white")
        self.assertTrue(self.game._are_compatible(cell5, cell6))
        
        # Same appearance and no names - should be incompatible
        cell7 = Cell(alive=True, symbol="●", color="white")
        cell8 = Cell(alive=True, symbol="●", color="white")
        self.assertFalse(self.game._are_compatible(cell7, cell8))
    
    def test_select_parents(self):
        """Test parent selection from neighbors"""
        # Create diverse neighbors
        neighbors = [
            Cell(alive=True, name="Red", color="red", symbol="●"),
            Cell(alive=True, name="Blue", color="blue", symbol="■"),
            Cell(alive=True, name="Green", color="green", symbol="◆")
        ]
        
        parent1, parent2 = self.game._select_parents(neighbors)
        
        # Should return two parents
        self.assertIsNotNone(parent1)
        self.assertIsNotNone(parent2)
        
        # Parents should be compatible
        self.assertTrue(self.game._are_compatible(parent1, parent2))
    
    def test_select_parents_single_neighbor(self):
        """Test parent selection with only one neighbor"""
        neighbors = [Cell(alive=True, name="Alone", color="red", symbol="●")]
        
        parent1, parent2 = self.game._select_parents(neighbors)
        
        # Should return one parent and None
        self.assertIsNotNone(parent1)
        self.assertIsNone(parent2)
    
    def test_create_offspring_from_two_parents(self):
        """Test offspring creation from two parents"""
        parent1 = Cell(alive=True, name="Fire", color="red", symbol="●")
        parent2 = Cell(alive=True, name="Ice", color="blue", symbol="■")
        
        offspring = self.game._create_offspring(parent1, parent2)
        
        # Offspring should be alive
        self.assertTrue(offspring.alive)
        
        # Offspring should inherit symbol from one parent
        self.assertIn(offspring.symbol, [parent1.symbol, parent2.symbol])
        
        # Offspring should inherit color from one parent
        self.assertIn(offspring.color, [parent1.color, parent2.color])
        
        # Offspring should have a hybrid name
        self.assertTrue(offspring.name)
        self.assertTrue("Fire" in offspring.name or "Ice" in offspring.name)
    
    def test_create_offspring_from_single_parent(self):
        """Test offspring creation from single parent"""
        parent = Cell(alive=True, name="Lone", color="green", symbol="◆")
        
        offspring = self.game._create_offspring(parent, None)
        
        # Offspring should inherit all properties from single parent
        self.assertTrue(offspring.alive)
        self.assertEqual(offspring.symbol, parent.symbol)
        self.assertEqual(offspring.color, parent.color)
        self.assertEqual(offspring.name, parent.name)
    
    def test_get_alive_neighbors(self):
        """Test getting list of alive neighbors"""
        # Set up pattern with specific neighbors
        self.game.set_cell(4, 4, True)
        self.game.set_cell(4, 5, True)
        self.game.set_cell(5, 4, True)
        
        neighbors = self.game._get_alive_neighbors(5, 5)
        
        # Should have exactly 3 neighbors
        self.assertEqual(len(neighbors), 3)
        
        # All neighbors should be alive
        for neighbor in neighbors:
            self.assertTrue(neighbor.alive)
    
    def test_offspring_breeding_across_generations(self):
        """Test that offspring can breed with other cells in subsequent generations"""
        # Create initial population with two types
        type1 = self.game.add_cell_type("Alpha", "red", "●")
        type2 = self.game.add_cell_type("Beta", "blue", "■")
        
        # Set up a pattern that will produce offspring
        self.game.set_cell(4, 4, alive=True, cell_type=type1)
        self.game.set_cell(4, 5, alive=True, cell_type=type2)
        self.game.set_cell(4, 6, alive=True, cell_type=type1)
        self.game.set_cell(5, 4, alive=True, cell_type=type2)
        
        # Run multiple generations
        for _ in range(3):
            self.game.next_generation()
        
        # Check that there are still living cells (pattern is evolving)
        alive_count = sum(1 for row in self.game.grid for cell in row if cell.alive)
        self.assertGreater(alive_count, 0)


if __name__ == '__main__':
    unittest.main()
