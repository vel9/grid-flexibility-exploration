import unittest
from allocator import allocate_resources

class AllocatorTestCase(unittest.TestCase):
    def test_allocate_resources_by_different_priorities(self):
        resources = [
            {"name": "A", "hours": 1, "priority": 3},
            {"name": "B", "hours": 1, "priority": 2},
            {"name": "C", "hours": 1, "priority": 1},
        ]
        slots = [
            ["Slot 1", 1],
            ["Slot 2", 2],
            ["Slot 3", 3],
        ]
        result = allocate_resources(resources, slots)
        self.assertEqual(3, len(result))
        self.assertEqual("C", result[0][0]) # Resource C was prioritized
        self.assertEqual("B", result[1][0])
        self.assertEqual("A", result[2][0])

    def test_allocate_resources_by_num_resources_less_than_slots(self):
        resources = [
            {"name": "A", "hours": 1, "priority": 3},
            {"name": "B", "hours": 1, "priority": 2},
            {"name": "C", "hours": 1, "priority": 1},
        ]
        slots = [
            ["Slot 1", 1],
            ["Slot 2", 2],
            ["Slot 3", 3],
            ["Slot 4", 4],
        ]
        result = allocate_resources(resources, slots)
        self.assertEqual(4, len(result))
        self.assertEqual("Unallocated", result[3][0])

    def test_allocate_resources_by_num_resources_more_than_slots(self):
        resources = [
            {"name": "A", "hours": 1, "priority": 3},
            {"name": "B", "hours": 1, "priority": 2},
            {"name": "C", "hours": 1, "priority": 1},
        ]
        slots = [
            ["Slot 1", 1],
            ["Slot 2", 2],
        ]
        with self.assertRaises(ValueError):
            allocate_resources(resources, slots)

if __name__ == '__main__':
    unittest.main()
