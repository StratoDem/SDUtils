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
