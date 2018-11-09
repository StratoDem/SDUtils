"""
File: sd_checks.py

Description:
Principal Author(s):
Secondary Author(s):

Notes:

November 28, 2016
StratoDem Analytics, LLC
"""

from typing import Any, Union, List

import dask.dataframe
import geopandas
import numpy as np
import pandas
import xarray

__all__ = [
    'T_INT', 'T_FLOAT', 'T_NUM',
    'T_DS', 'T_DF',
    'T_DDF', 'T_DDS',

    'T_ARRAY',

    'T_INT_GENERIC', 'T_FLOAT_GENERIC', 'T_NUM_GENERIC',

    'T_COL',

    'check_ds', 'check_df', 'check_gdf', 'check_xds', 'check_xda',
    'check_ddf', 'check_dds',
    'check_ndarray',

    'assert_t_col'
]

# /// type definitions /// #
T_INT = Union[int, np.int64]
T_FLOAT = Union[float, np.float64]
T_NUM = Union[T_INT, T_FLOAT]

T_DS = pandas.Series
T_DF = pandas.DataFrame
T_GDF = geopandas.GeoDataFrame
T_XDA = xarray.DataArray
T_XDS = xarray.Dataset

T_DDS = dask.dataframe.Series
T_DDF = dask.dataframe.DataFrame

T_ARRAY = Union[T_DS, T_DF, np.ndarray]

T_INT_GENERIC = Union[T_INT, T_ARRAY]
T_FLOAT_GENERIC = Union[T_FLOAT, T_ARRAY]
T_NUM_GENERIC = Union[T_NUM, T_ARRAY]


# /// other type definitions /// #
T_COL = Union[str, List[str]]


# /// data type checking functions /// #
def check_ds(ds: Any, msg: str='Is not a Series') -> T_DS:
    assert isinstance(msg, str)
    assert isinstance(ds, pandas.Series), msg
    return ds.copy()


def check_df(df: Any, msg: str='Is not a DataFrame') -> T_DF:
    assert isinstance(msg, str)
    assert isinstance(df, pandas.DataFrame), msg
    return df.copy()


def check_gdf(df: Any, msg: str='Is not a GeoDataFrame') -> T_GDF:
    assert isinstance(msg, str)
    assert isinstance(df, geopandas.GeoDataFrame), msg
    return df.copy()


def check_xds(xds: Any, msg: str='Is not a Dataset') -> T_XDS:
    assert isinstance(msg, str)
    assert isinstance(xds, xarray.Dataset), msg
    return xds.copy()


def check_xda(xda: Any, msg: str='Is not a DataArray') -> T_XDA:
    assert isinstance(msg, str)
    assert isinstance(xda, xarray.DataArray), msg
    return xda.copy()


def check_ddf(ddf: Any, msg: str='Is not a dask DataFrame') -> T_DDF:
    assert isinstance(msg, str)
    assert isinstance(ddf, dask.dataframe.DataFrame), msg
    return ddf.copy()


def check_dds(dds: Any, msg: str='Is not a dask Series') -> T_DDS:
    assert isinstance(msg, str)
    assert isinstance(dds, dask.dataframe.Series), msg
    return dds.copy()


def check_ndarray(nd: Any, msg: str='Is not an ndarray') -> np.ndarray:
    assert isinstance(msg, str)
    assert isinstance(nd, np.ndarray), msg
    return nd.copy()


# /// other type checking functions
def assert_t_col(t_col: Any) -> T_COL:
    assert isinstance(t_col, str) or \
           (isinstance(t_col, list) and all(isinstance(c, str) for c in t_col))
    return t_col
