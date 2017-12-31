"""
StratoDem Analytics : base_test
Principal Author(s) : Michael Clawar
Secondary Author(s) :
Description :

Notes :

December 14, 2017
"""

import os
import unittest

import pandas


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self._df = pandas.DataFrame([
            ('A', 1, 'test', 1.3),
            ('B', 2, 'test2', 1.5),
            ('C', 3, 'test3', 1.2),
            ('D', 4, 'test4', 1.1),
        ], columns=['COL_STR', 'COL_INT', 'COL_STR_2', 'COL_FLOAT'])
        self._df.index = [2, 3, 4, 5]

        file_format_str = '__TESTING_FILE_1234.{extension}'
        self._temporary_parquet_file_path = file_format_str.format(extension='parquet')

    def tearDown(self):
        if os.path.isfile(self._temporary_parquet_file_path):
            print('Removing {}'.format(self._temporary_parquet_file_path))
            os.remove(self._temporary_parquet_file_path)
