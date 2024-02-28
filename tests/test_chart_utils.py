import unittest
from chart_utils import get_average_in_column
import pandas as pd

class ChartUtilsTestCase(unittest.TestCase):
    def test_get_average_in_column(self):
        col_name = "col_to_average"
        data = {col_name: [5, 15, 10]}
        data_df = pd.DataFrame(data)
        self.assertEqual(10, get_average_in_column(data_df, col_name))  # add assertion here

if __name__ == '__main__':
    unittest.main()
