"""
File: sd_xds.py

Description:
Principal Author(s):
Secondary Author(s):

Notes:

January 12, 2017
StratoDem Analytics, LLC
"""

from typing import List, Union

import numpy as np
import pandas
import xarray


__all__ = ['df_to_xds', 'ds_to_xda', 'make_gather_map']


def df_to_xds(df: pandas.DataFrame) -> xarray.Dataset:
    assert isinstance(df, pandas.DataFrame)
    return xarray.Dataset.from_dataframe(df)


def ds_to_xda(ds: pandas.Series) -> xarray.DataArray:
    assert isinstance(ds, pandas.Series)
    return xarray.DataArray.from_series(ds)


def make_gather_map(xda_reference: xarray.DataArray,
                    gather_values: Union[xarray.DataArray, np.ndarray, List]) -> List[int]:
    assert isinstance(xda_reference, xarray.DataArray)

    g5_to_idx = {g5: idx for idx, g5 in enumerate(xda_reference.values)}

    if isinstance(gather_values, xarray.DataArray):
        return [g5_to_idx[g5_to] for g5_to in gather_values.values]
    elif isinstance(gather_values, (np.ndarray, list)):
        # noinspection PyTypeChecker
        return [g5_to_idx[g5_to] for g5_to in gather_values]
    else:
        raise TypeError
