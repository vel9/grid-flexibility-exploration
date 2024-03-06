import unittest
from allocator import allocate_resources
from allocator import allocate_resources_parallel
from allocator import to_resources

class AllocatorTestCase(unittest.TestCase):
    def test_allocate_resources_by_different_priorities(self):
        resources = to_resources([
            {"name": "A", "hours": 1, "priority": 3},
            {"name": "B", "hours": 1, "priority": 2},
            {"name": "C", "hours": 1, "priority": 1},
        ])
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
        resources = to_resources([
            {"name": "A", "hours": 1, "priority": 3},
            {"name": "B", "hours": 1, "priority": 2},
            {"name": "C", "hours": 1, "priority": 1},
        ])
        slots = [
            ["Slot 1", 1],
            ["Slot 2", 2],
            ["Slot 3", 3],
            ["Slot 4", 4],
        ]
        result = allocate_resources(resources, slots)
        self.assertEqual(4, len(result))
        self.assertEqual("Nothing Scheduled", result[3][0])

    def test_allocate_resources_by_num_resources_more_than_slots(self):
        resources = to_resources([
            {"name": "A", "hours": 1, "priority": 3},
            {"name": "B", "hours": 1, "priority": 2},
            {"name": "C", "hours": 1, "priority": 1},
        ])
        slots = [
            ["Slot 1", 1],
            ["Slot 2", 2],
        ]
        with self.assertRaises(ValueError):
            allocate_resources(resources, slots)

    def test_allocate_resources_parallel_by_single_resource_across_multiple_hours(self):
        resources = to_resources([
            {"name": "A", "hours": 2, "priority": 1, "demand_per_hour": 1},
        ])
        slots = [
            ["Slot 1", 5],
            ["Slot 2", 1],
        ]
        result = allocate_resources_parallel(resources, slots)
        self.assertEqual(3, len(result))

        # resource A was allocated to first slot
        self.assertEqual("Slot 1", result[0][1])
        self.assertEqual("A", result[0][0]) # resource 1 scheduled
        self.assertEqual(1, result[0][2])

        # since resources are scheduled across slots, 4 of the units should stay unallocated
        self.assertEqual("Nothing Scheduled", result[1][0])
        self.assertEqual("Slot 1", result[1][1])
        self.assertEqual(4, result[1][2])

        # resource A was also allocated to second slot
        self.assertEqual("Slot 2", result[2][1])
        self.assertEqual("A", result[2][0]) # resource B scheduled
        self.assertEqual(1, result[2][2])

    def test_allocate_resources_parallel_by_multiple_resources_across_multiple_hours(self):
        resources = to_resources([
            {"name": "A", "hours": 1, "priority": 1, "demand_per_hour": 1},
            {"name": "B", "hours": 2, "priority": 2, "demand_per_hour": 2},
        ])
        slots = [
            ["Slot 1", 6],
            ["Slot 2", 2],
        ]
        result = allocate_resources_parallel(resources, slots)
        self.assertEqual(4, len(result))

        # resource A was allocated to first slot
        self.assertEqual("Slot 1", result[0][1])
        self.assertEqual("A", result[0][0])
        self.assertEqual(1, result[0][2])

        # resource B was also allocated to first slot
        self.assertEqual("B", result[1][0])
        self.assertEqual("Slot 1", result[1][1])
        self.assertEqual(2, result[1][2])

        self.assertEqual("Nothing Scheduled", result[2][0])
        self.assertEqual("Slot 1", result[2][1])
        self.assertEqual(3, result[2][2])

        # resource B was also allocated to second slot
        self.assertEqual("B", result[3][0])
        self.assertEqual("Slot 2", result[3][1])
        self.assertEqual(2, result[3][2])

if __name__ == '__main__':
    unittest.main()
