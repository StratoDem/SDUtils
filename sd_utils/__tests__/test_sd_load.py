"""
StratoDem Analytics : test_sd_load
Principal Author(s) : Michael Clawar
Secondary Author(s) :
Description :

Notes :

December 14, 2017
"""

import unittest

from .base_test import BaseTestCase

import sd_utils.sd_load as sdl


class TestSDLoad(BaseTestCase):
    def test_parquet_write_load(self):
        # Full write
        sdl.write_df_parquet(self._df, self._temporary_parquet_file_path)

        df = sdl.read_df_parquet(self._temporary_parquet_file_path)
        self.assertTrue(a == b for a, b in zip(df.columns, self._df.columns))

        self.assertTrue(df['COL_STR'].eq(self._df['COL_STR']).all())
        self.assertTrue(df['COL_INT'].eq(self._df['COL_INT']).all())
        self.assertTrue(df['COL_STR_2'].eq(self._df['COL_STR_2']).all())
        self.assertTrue(df['COL_FLOAT'].eq(self._df['COL_FLOAT']).all())

        # Only read two columns
        df = sdl.read_df_parquet(
            self._temporary_parquet_file_path, columns=['COL_STR', 'COL_FLOAT'])
        self.assertTrue(a == b for a, b in zip(df.columns, ['COL_STR', 'COL_FLOAT']))

        self.assertTrue(df['COL_STR'].eq(self._df['COL_STR']).all())
        self.assertTrue(df['COL_FLOAT'].eq(self._df['COL_FLOAT']).all())
        with self.assertRaises(KeyError):
            _ = df['COL_INT']
        with self.assertRaises(KeyError):
            _ = df['COL_STR_2']
