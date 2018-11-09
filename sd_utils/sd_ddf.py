"""
File: sd_ddf

Description:
Principal Author(s):
Secondary Author(s):

Notes:

June 06, 2017
StratoDem Analytics, LLC
"""

import dask
import dask.dataframe
import dask.multiprocessing
import pandas

from sd_utils.sd_config import SDConfig


__all__ = ['df_to_ddf', 'ddf_checkpoint']


T_DDF = dask.dataframe.DataFrame


def df_to_ddf(df: pandas.DataFrame, *, npartitions: int=SDConfig.npartitions) -> T_DDF:
    assert isinstance(df, pandas.DataFrame)
    assert isinstance(npartitions, int)
    return dask.dataframe.from_pandas(df, npartitions=npartitions)


def ddf_checkpoint(ddf: T_DDF, *, npartitions: int=SDConfig.npartitions) -> T_DDF:
    assert isinstance(ddf, dask.dataframe.DataFrame)
    assert isinstance(npartitions, int)
    return df_to_ddf(ddf.compute())
