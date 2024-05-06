import unittest
from memory_bank.src.context_manager import ContextManager

class TestContextManager(unittest.TestCase):

    def setUp(self):
        # Initialize a ContextManager instance for testing
        self.context_manager = ContextManager()

    def test_add_memory(self):
        # Test adding a memory to the memory bank
        self.context_manager.add_memory("Test Memory", "This is a test memory.")
        # Retrieve the memory added
        memory = self.context_manager.get_memory_by_id(1)
        # Check if the memory details match
        self.assertEqual(memory['title'], "Test Memory")
        self.assertEqual(memory['description'], "This is a test memory.")

    def test_delete_memory(self):
        # Add a memory to the memory bank for testing
        self.context_manager.add_memory("Test Memory", "This is a test memory.")
        # Delete the memory
        self.context_manager.delete_memory(1)
        # Try to retrieve the deleted memory
        memory = self.context_manager.get_memory_by_id(1)
        # Check if the memory is None (deleted)
        self.assertIsNone(memory)

    def test_get_memory_by_id(self):
        # Add a memory to the memory bank for testing
        self.context_manager.add_memory("Test Memory", "This is a test memory.")
        # Retrieve the memory by ID
        memory = self.context_manager.get_memory_by_id(1)
        # Check if the retrieved memory is not None
        self.assertIsNotNone(memory)
        # Check if the memory details match
        self.assertEqual(memory['title'], "Test Memory")
        self.assertEqual(memory['description'], "This is a test memory.")

    def test_get_all_memories(self):
        # Add multiple memories to the memory bank for testing
        self.context_manager.add_memory("Memory 1", "Description 1")
        self.context_manager.add_memory("Memory 2", "Description 2")
        self.context_manager.add_memory("Memory 3", "Description 3")
        # Retrieve all memories
        memories = self.context_manager.get_all_memories()
        # Check if the number of retrieved memories is correct
        self.assertEqual(len(memories), 3)

    def tearDown(self):
        # Clean up after each test by resetting the memory bank
        self.context_manager.reset()

if __name__ == '__main__':
    unittest.main()
