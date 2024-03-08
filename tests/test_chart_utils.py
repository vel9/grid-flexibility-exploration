import unittest
from chart_utils import get_average_in_column
import pandas as pd


class ChartUtilsTestCase(unittest.TestCase):

    def test_get_average_in_column_by_empty_values(self):
        col_name = "col_to_average"
        data = {col_name: []}
        data_df = pd.DataFrame(data)
        with self.assertRaises(ValueError):
            get_average_in_column(data_df, col_name)

    def test_get_average_in_column_by_one_value(self):
        col_name = "col_to_average"
        data = {col_name: [5]}
        data_df = pd.DataFrame(data)
        self.assertEqual(5, get_average_in_column(data_df, col_name))

    def test_get_average_in_column_by_three_values(self):
        col_name = "col_to_average"
        data = {col_name: [5, 15, 10]}
        data_df = pd.DataFrame(data)
        self.assertEqual(10, get_average_in_column(data_df, col_name))


if __name__ == '__main__':
    unittest.main()
