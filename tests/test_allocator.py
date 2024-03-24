import unittest

import pandas as pd
from pandas import Timestamp

from allocator import allocate_resources_parallel
from allocator import to_resources
from allocator import get_window_size
from allocator import allocate_resources_by_min_rolling_average


class AllocatorTestCase(unittest.TestCase):

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
        self.assertEqual("A", result[0][0])  # resource 1 scheduled
        self.assertEqual(1, result[0][2])

        # since resources are scheduled across slots, 4 of the units should stay unallocated
        self.assertEqual("Nothing Scheduled", result[1][0])
        self.assertEqual("Slot 1", result[1][1])
        self.assertEqual(4, result[1][2])

        # resource A was also allocated to second slot
        self.assertEqual("Slot 2", result[2][1])
        self.assertEqual("A", result[2][0])  # resource B scheduled
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

    def test_get_window_size_by_invalid_num_hours(self):
        with self.assertRaises(ValueError):
            get_window_size(0, 5)

    def test_get_window_size_by_invalid_num_minutes_in_interval(self):
        with self.assertRaises(ValueError):
            get_window_size(5, 0)

    def test_get_window_size_by_whole_hour(self):
        self.assertEqual(12, get_window_size(1, 5))
        self.assertEqual(24, get_window_size(2, 5))


    def test_allocate_resources_by_min_rolling_average(self):
        num_mins_in_interval = 60
        resources = to_resources([
            {"name": "A", "hours": 2, "priority": 3},
        ])
        slots = []
        for interval in range(24):
            slots.append([add_hours('20240308', interval), 17])
        slots[23][1] = 5  # force last window to be optimal

        slots_df = pd.DataFrame(slots, columns=["Time", "Value"])
        result = allocate_resources_by_min_rolling_average(resources, slots_df, num_mins_in_interval)
        # make sure we select our last generated timestamp as end of optimal window
        self.assertEqual(add_hours('20240308', 23), result[1][1])
        self.assertEqual(add_hours('20240308', 22), result[0][1])
        self.assertEqual(11, result[1][2]) # 17 + 5 / 2 = 11


def add_hours(time_str, num_hours):
    return Timestamp(time_str) + pd.Timedelta(hours=num_hours)

if __name__ == '__main__':
    unittest.main()
