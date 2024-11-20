import unittest
from .fuzzyItemSearch import FuzzyItemSearch,
from .types import WorldState

class TestFuzzyItemSearch(unittest.TestCase):
    def setUp(self):
        """Set up the items list and a FuzzyItemSearch instance."""
        # Items structured as categories of lists, each item has a name
        self.items = [
            [{"name": "apple"}, {"name": "banana"}, {"name": "cherry"}],
            [{"name": "date"}, {"name": "elderberry"}],
            [{"name": "fig"}, {"name": "grape"}]
        ]

        # Create the search tool
        self.search_tool = FuzzyItemSearch(buffer="an", items=self.items)

    def test_matches(self):
        """Test the matches method."""
        self.assertTrue(self.search_tool.matches("banana"))
        self.assertFalse(self.search_tool.matches("fig"))

    def test_searchForward(self):
        """Test searching forward."""
        # Starting from the first item
        initial_state = WorldState(categoryIndex=0, itemIndex=0)
        new_state = self.search_tool.searchForward(initial_state)
        self.assertEqual(new_state, WorldState(categoryIndex=0, itemIndex=1))  # "banana" matches

        # Test reaching the end of the list
        initial_state = WorldState(categoryIndex=2, itemIndex=1)
        new_state = self.search_tool.searchForward(initial_state)
        self.assertIsNone(new_state)  # No more matches

    def test_searchBackward(self):
        """Test searching backward."""
        # Starting from the middle
        initial_state = WorldState(categoryIndex=1, itemIndex=1)
        new_state = self.search_tool.searchBackward(initial_state)
        self.assertEqual(new_state, WorldState(categoryIndex=0, itemIndex=1))  # "banana" matches

        # Test reaching the beginning of the list
        initial_state = WorldState(categoryIndex=0, itemIndex=0)
        new_state = self.search_tool.searchBackward(initial_state)
        self.assertIsNone(new_state)  # No matches before the start

    def test_searchFirst(self):
        """Test searching for the first match."""
        new_state = self.search_tool.searchFirst()
        self.assertEqual(new_state, WorldState(categoryIndex=0, itemIndex=1))  # "banana" matches

    def test_searchFromHere(self):
        """Test searching from a specific state."""
        # Starting from a matching state
        initial_state = WorldState(categoryIndex=1, itemIndex=1)
        new_state = self.search_tool.searchFromHere(initial_state)
        self.assertEqual(new_state, WorldState(categoryIndex=1, itemIndex=1))  # "elderberry" matches

        # Test a state that doesn’t match
        self.search_tool.buffer = "nonexistent"
        initial_state = WorldState(categoryIndex=0, itemIndex=0)
        new_state = self.search_tool.searchFromHere(initial_state)
        self.assertIsNone(new_state)  # No matches for "nonexistent"

if __name__ == "__main__":
    unittest.main()
