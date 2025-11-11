"""
Unit tests for Conway's Game of Life implementation
"""

import unittest
from game_of_life import GameOfLife


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
                self.assertFalse(cell)
    
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
                self.assertFalse(cell)
    
    def test_load_pattern_glider(self):
        """Test loading the glider pattern"""
        result = self.game.load_pattern('glider')
        self.assertTrue(result)
        
        # Check that some cells are alive
        alive_count = sum(sum(row) for row in self.game.grid)
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


if __name__ == '__main__':
    unittest.main()
