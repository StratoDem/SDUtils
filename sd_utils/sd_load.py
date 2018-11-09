"""
File: sd_load.py

Description: Loading helpers
Principal Author(s): Michael Clawar
Secondary Author(s):

Notes:

December 12, 2016
StratoDem Analytics, LLC
"""

import functools
import multiprocessing
import os
import warnings
from io import StringIO
from typing import Callable, Optional, List, Iterable

import dask.dataframe
import joblib
import geopandas
import pandas
import simpledbf
import xarray

from . import sd_log, sd_checks
from sd_utils.sd_config import SDConfig


__all__ = [
    'read_df_csv', 'read_df_json', 'read_df_fwf', 'read_df_hdf', 'read_df_stata', 'read_df_dbf',
    'read_df_geopandas', 'read_df_excel', 'read_df_parquet', 'read_ddf_parquet',

    'multi_read_df_csv', 'multi_read_df_fwf', 'multi_read_df_geopandas', 'multi_read_df_excel',
    'multi_read_df_stata',
    'multi_joblib_read_df_csv',

    'write_df_csv', 'write_df_csv_stringio', 'write_df_hdf', 'write_df_parquet',
    'write_ddf_parquet',

    'read_xds_netcdf',
    'write_xds_netcdf',

    'file_size',
]


T_DF = sd_checks.T_DF
T_GDF = sd_checks.T_GDF
T_DDF = sd_checks.T_DDF

T_CB = Callable[[T_DF, str], T_DF]


# ///// Read DF - Normal /////
@sd_log.log_func
def read_df_csv(csv_file_path: str, *, callback: Optional[T_CB]=None, **pandas_kwargs) -> T_DF:
    """Standard csv loading function. Can be used for almost all csv files"""
    assert isinstance(csv_file_path, str)
    assert callback is None or callable(callback)

    df_iter = pandas.read_csv(csv_file_path, iterator=True, chunksize=100000, **pandas_kwargs)
    df = pandas.concat(df_iter, ignore_index=True)

    if callable(callback):
        df = callback(df=df, file_path=csv_file_path)

    return sd_checks.check_df(df)


@sd_log.log_func
def read_df_json(json_file_path: str, **kwargs) -> T_DF:
    """Standard pandas json loading function."""
    assert isinstance(json_file_path, str)

    df = pandas.read_json(json_file_path, **kwargs)
    return sd_checks.check_df(df)


@sd_log.log_func
def read_df_fwf(fwf_file_path: str, **pandas_kwargs) -> T_DF:
    """Standard fixed-width format reader function. Can be used for almost all fwf files"""
    assert isinstance(fwf_file_path, str)

    # Iterative loading because python has a bug when loading giant text files
    df_iter = pandas.read_fwf(fwf_file_path, iterator=True, chunksize=100000, **pandas_kwargs)
    df = pandas.concat(df_iter, ignore_index=True)
    return sd_checks.check_df(df)


@sd_log.log_func
def read_df_hdf(hdf_file: str, hdf_key: str, *, columns: Optional[List[str]]=None,
                where: Optional[str]=None) -> T_DF:
    assert isinstance(hdf_file, str)
    assert os.path.isfile(hdf_file)
    assert isinstance(hdf_key, str)
    assert columns is None or isinstance(columns, list)
    assert columns is None or all(isinstance(c, str) for c in columns)
    assert where is None or isinstance(where, str)

    return pandas.read_hdf(hdf_file, hdf_key, columns=columns, where=where)


@sd_log.log_func
def read_df_stata(stata_file: str, callback: Optional[T_CB], **pandas_kwargs) -> T_DF:
    assert isinstance(stata_file, str)
    assert callback is None or callable(callback)

    df = pandas.read_stata(stata_file, **pandas_kwargs)

    if callable(callback):
        df = callback(df=df, file_path=stata_file)

    return sd_checks.check_df(df)


@sd_log.log_func
def read_df_dbf(dbf_file: str, **simpledbf_kwargs) -> T_DF:
    assert isinstance(dbf_file, str)
    dbf = simpledbf.Dbf5(dbf_file, **simpledbf_kwargs)
    df = pandas.concat((df for df in dbf.to_dataframe(chunksize=10000)), ignore_index=True)
    return sd_checks.check_df(df)


@sd_log.log_func
def read_df_geopandas(file_path, *, callback: Optional[T_CB]=None, **geopandas_kwargs) -> T_GDF:
    assert isinstance(file_path, str)
    sd_log.log(file_path)

    gdf = geopandas.read_file(file_path, **geopandas_kwargs)

    if callable(callback):
        gdf = callback(df=gdf, file_path=file_path)

    return sd_checks.check_gdf(gdf)


@sd_log.log_func
def read_df_excel(file_path, *,
                  callback: Optional[T_CB]=None,
                  **pandas_kwargs) -> T_DF:
    assert isinstance(file_path, str)
    assert callback is None or callable(callback)
    sd_log.log(file_path)

    df = pandas.read_excel(file_path, **pandas_kwargs)
    assert isinstance(df, pandas.DataFrame)

    if callable(callback):
        df = callback(df=df, file_path=file_path)
        assert isinstance(df, pandas.DataFrame), 'callback must return a pandas DataFrame'

    return df


@sd_log.log_func
def read_df_parquet(file_path: str, columns: Optional[Iterable[str]]=None,
                    use_threads: bool=True, **pyarrow_kwargs) -> T_DF:
    assert isinstance(file_path, str), '{} does not exist'.format(file_path)
    assert os.path.exists(file_path), 'file does not exist at {}'.format(file_path)
    assert columns is None or isinstance(columns, (list, tuple))
    assert columns is None or all(isinstance(c, str) for c in columns)
    assert isinstance(use_threads, bool)

    df = pandas.read_parquet(file_path, engine='pyarrow', use_threads=use_threads, columns=columns,
                             **pyarrow_kwargs)

    # df = pyarrow.parquet.read_table(file_path, nthreads=n_threads, columns=columns,
    #                                 **pyarrow_kwargs) \
    #     .to_pandas(nthreads=n_threads)

    return df


@sd_log.log_func
def read_ddf_parquet(file_path: str, columns: Optional[Iterable[str]]=None,
                     **dd_kwargs) -> T_DDF:
    assert isinstance(file_path, str), '{} does not exist'.format(file_path)
    assert os.path.exists(file_path), 'file does not exist at {}'.format(file_path)
    assert columns is None or isinstance(columns, (list, tuple))
    assert columns is None or all(isinstance(c, str) for c in columns)

    return dask.dataframe.read_parquet(path=file_path, columns=columns, engine='arrow',
                                       **dd_kwargs)


# ///// Read DF - Multi ///// #
def _multi_read_df_generic(paths: List[str], read_func: Callable, *,
                           pool_size: int=SDConfig.cpu_count, callback: Optional[T_CB]=None,
                           **pandas_kwargs) -> T_DF:
    assert isinstance(paths, (tuple, list))
    assert all(isinstance(p, str) for p in paths)
    assert callable(read_func)
    assert isinstance(pool_size, int)
    assert callback is None or callable(callback)

    partial_func = functools.partial(read_func, callback=callback, **pandas_kwargs)

    if len(paths) == 1:
        return partial_func(paths[0])

    if len(paths) == 2:
        df = pandas.concat([partial_func(paths[0]), partial_func(paths[1])], ignore_index=True)
        return sd_checks.check_df(df)

    with multiprocessing.Pool(pool_size) as pool:
        df_list = pool.map(partial_func, paths, chunksize=1)
        df = pandas.concat(df_list, ignore_index=True)

        return sd_checks.check_df(df)


def _multi_joblib_read_df_generic(paths: List[str], read_func: Callable,
                                  kwargs_dict_list: List[dict], *,
                                  pool_size: int=SDConfig.cpu_count,
                                  callback: Optional[T_CB]=None, **pandas_kwargs) -> T_DF:
    assert isinstance(paths, (tuple, list))
    assert all(isinstance(p, str) for p in paths)
    assert callable(read_func)
    assert isinstance(kwargs_dict_list, (tuple, list))
    assert all(isinstance(d, dict) for d in kwargs_dict_list)
    assert isinstance(pool_size, int)
    assert callback is None or callable(callback)
    assert len(paths) == len(kwargs_dict_list)

    partial_func = functools.partial(read_func, callback=callback, **pandas_kwargs)

    if len(paths) == 1:
        return partial_func(paths[0], **kwargs_dict_list[0])

    df_list = joblib.Parallel(pool_size)(
        joblib.delayed(partial_func)(p, **d) for p, d in zip(paths, kwargs_dict_list))
    df = pandas.concat(df_list, ignore_index=True)
    return sd_checks.check_df(df)


@sd_log.log_func
def multi_read_df_csv(paths: List[str], *, pool_size: int=SDConfig.cpu_count,
                      callback: Optional[T_CB]=None, **pandas_kwargs) -> T_DF:
    return _multi_read_df_generic(paths, read_func=read_df_csv, pool_size=pool_size,
                                  callback=callback, **pandas_kwargs)


@sd_log.log_func
def multi_joblib_read_df_csv(paths: List[str], kwargs_dict_list: List[dict], *,
                             pool_size: int=SDConfig.cpu_count,
                             callback: Optional[T_CB]=None, **pandas_kwargs) -> T_DF:
    return _multi_joblib_read_df_generic(
        paths, read_func=read_df_csv, kwargs_dict_list=kwargs_dict_list,
        pool_size=pool_size, callback=callback, **pandas_kwargs)


@sd_log.log_func
def multi_read_df_fwf(paths: List[str], *, pool_size: int=SDConfig.cpu_count,
                      callback: Optional[T_CB]=None, **pandas_kwargs) -> T_DF:
    return _multi_read_df_generic(paths, read_func=read_df_fwf, pool_size=pool_size,
                                  callback=callback, **pandas_kwargs)


@sd_log.log_func
def multi_read_df_geopandas(paths: List[str], *, pool_size: int=SDConfig.cpu_count,
                            callback: Optional[T_CB] = None, **geopandas_kwargs) -> T_GDF:
    df = _multi_read_df_generic(paths, read_func=read_df_geopandas, pool_size=pool_size,
                                callback=callback, **geopandas_kwargs)
    return sd_checks.check_gdf(df)


@sd_log.log_func
def multi_read_df_excel(paths: List[str], *, pool_size: int=SDConfig.cpu_count,
                        callback: Optional[T_CB]=None, **pandas_kwargs) -> T_DF:
    return _multi_read_df_generic(paths, read_func=read_df_excel, pool_size=pool_size,
                                  callback=callback, **pandas_kwargs)


@sd_log.log_func
def multi_read_df_stata(paths: List[str], *, pool_size: int=SDConfig.cpu_count,
                        callback: Optional[T_CB]=None, **pandas_kwargs) -> T_DF:
    return _multi_read_df_generic(paths, read_func=read_df_stata, pool_size=pool_size,
                                  callback=callback, **pandas_kwargs)


# ///// Write DF///// #
@sd_log.log_func
def write_df_csv(df: T_DF, csv_file: str, **kwargs) -> None:
    """

    Parameters
    ----------
    df: pandas.DataFrame
    csv_file: str
    kwargs:
        kwargs to to_csv for a pandas.DataFrame
    """
    assert isinstance(df, pandas.DataFrame)
    assert isinstance(csv_file, str)
    kwargs = {**dict(index=False, chunksize=25000), **kwargs}
    df.to_csv(csv_file, **kwargs)


@sd_log.log_func
def write_df_csv_stringio(df: T_DF, **kwargs) -> StringIO:
    assert isinstance(df, pandas.DataFrame)
    kwargs = {**dict(index=False, chunksize=50000), **kwargs}

    s_buf = StringIO()
    df.to_csv(s_buf, **kwargs)
    s_buf.seek(0)

    return s_buf


@sd_log.log_func
def write_df_hdf(df: T_DF, hdf_file: str, hdf_key: str, *,
                 append: bool=False, fast: bool=False, compress: bool=True,
                 min_itemsize: Optional[int]=None) -> None:
    """Write an hdf file for the current pandas.DataFrame"""
    assert isinstance(df, pandas.DataFrame)
    assert isinstance(hdf_file, str)
    assert isinstance(hdf_key, str)
    assert isinstance(append, bool)

    assert isinstance(fast, bool)
    assert isinstance(compress, bool)
    assert min_itemsize is None or isinstance(min_itemsize, int)

    if not fast:
        assert compress is True

        hdf_kwargs = dict(format='t', complib='lzo', data_columns=df.columns,
                          index=False, chunksize=75000, min_itemsize=min_itemsize)

        if not append:
            df.to_hdf(hdf_file, hdf_key, **hdf_kwargs)
        else:
            df.to_hdf(hdf_file, hdf_key, append=True, **hdf_kwargs)
    else:
        assert append is False
        assert min_itemsize is None

        fast_hdf_kwargs = dict(format='f', index=False, chunksize=75000)

        if compress:
            df.to_hdf(hdf_file, hdf_key, complib='lzo', **fast_hdf_kwargs)
        else:
            df.to_hdf(hdf_file, hdf_key, **fast_hdf_kwargs)


@sd_log.log_func
def write_df_parquet(df: T_DF, file_path: str, chunk_size: int=50000,
                     version: str='2.0', index: bool=True, **pyarrow_kwargs) -> None:
    assert isinstance(file_path, str)
    assert isinstance(chunk_size, int) and chunk_size > 0
    assert all(isinstance(c, str) for c in df.columns)

    if not index:
        df = df.reset_index(drop=True)

    df.to_parquet(
        file_path,
        engine='pyarrow',
        chunk_size=chunk_size,
        version=version,
        **pyarrow_kwargs)

    # noinspection PyArgumentList
    # df_arrow = pyarrow.Table.from_pandas(df)
    # pyarrow.parquet.write_table(
    #     df_arrow, file_path, chunk_size=chunk_size, version=version, **kwargs)


@sd_log.log_func
def write_ddf_parquet(ddf: T_DDF, file_path: str, **dd_kwargs) -> None:
    assert isinstance(file_path, str)
    assert all(isinstance(c, str) for c in ddf.columns)
    assert isinstance(ddf, dask.dataframe.DataFrame)

    ddf.to_parquet(path=file_path, **dd_kwargs)


# ///// xarray - read ///// #
@sd_log.log_func
def read_xds_netcdf(file_path: str, **xarray_kwargs) -> xarray.Dataset:
    assert isinstance(file_path, str)
    xds = xarray.open_dataset(file_path, **xarray_kwargs)
    assert isinstance(xds, xarray.Dataset)
    return xds


# /// xarray - writer /// #
@sd_log.log_func
def write_xds_netcdf(xds: xarray.Dataset, file_path: str, **xarray_kwargs) -> None:
    assert isinstance(xds, xarray.Dataset)
    assert isinstance(file_path, str)
    xds.to_netcdf(file_path, **xarray_kwargs)


# ///// Other ///// #
def file_size(file_path: str) -> int:
    assert isinstance(file_path, str)
    return os.stat(file_path).st_size
