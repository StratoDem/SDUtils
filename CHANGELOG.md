## [2.4.0] 2019-05-18
### Changes
- Dependencies updates:
    - `pyarrow` -> 0.15.1 [#172](https://github.com/StratoDem/SDUtils/pull/172)
    - `numpy` -> 1.17.4 [#173](https://github.com/StratoDem/SDUtils/pull/173)
    - `pandas` -> 0.25.3 [#171](https://github.com/StratoDem/SDUtils/pull/171)
    - `dask` -> 2.8.0 [#175](https://github.com/StratoDem/SDUtils/pull/175)

## [2.3.2] 2019-05-18
### Fixes
- Locks `pyarrow` to `0.12.0` to avoid segfault as described in https://github.com/pytorch/pytorch/issues/13039#issuecomment-481443691

## [2.3.1] 2019-05-18
### Fixes
- Fixes kwargs passed along to pyarrow/fastparquet engines in `read_df_parquet` and `read_ddf_parquet`
- Updates `write_df_parquet` and `write_ddf_parquet` to handle `fastparquet` engine

## [2.3.0] 2019-05-18
### Changes
- `read_df_parquet` and `read_ddf_parquet` now take optional `engine` argument to allow to use `pyarrow` or `fastparquet` engines for reading parquet files.

## [2.2.0] 2019-05-06
### Changes
- Updates `slackclient` dependency to `2.0.1` and handles migration of api to v2 (https://github.com/slackapi/python-slackclient/wiki/Migrating-to-2.x)

## [2.1.1] 2019-04-07
### Changes
- Updates requirements for `pandas`, `numpy`, `dask`, and `pyarrow`

## [2.1.0] 2019-01-18
### Changes
- Updates requirements for pandas, numpy, scikit-learn, and pyarrow

## [2.0.0] 2018-11-10
### Changed
- Updates `pyarrow` requirement to `0.11`
- Changes `nthreads` in `read_df_parquet` to `use_threads` to match https://arrow.apache.org/docs/python/generated/pyarrow.parquet.ParquetFile.html#pyarrow.parquet.ParquetFile.read

## [1.4.1] 2018-01-15
### Changed
- `SDLog` logs traceback up to 10 levels deep as text to Slack.

## [1.4.0] 2018-01-15
### Changed
- `SDLog` will now also log error traceback to Slack
(before it was only the type and the value).

## [1.3.1] 2018-01-15
### Changed
- Updated `pandas`, `dask`, and `numpy` versions.


## [1.3.0] 2018-01-15
### Added
- `SDLog` now uses a class `log_message` method to log -- this now
supports a custom logging interface by inheriting from `SDLog` or
replacing `log_message` in an application.
```python
class MyTestLogger(SDLog):
    @classmethod
    def log_message(cls, message: str, **kwargs):
        print('SPECIAL LOGGER', message)
```
This class will print 'SPECIAL LOGGER' before all messages, but otherwise
act the same as the normal `SDLog`. As another example, the `log_message`
method could connect to and log to a database for non-console-based
logging.
