[1.3.1] 2018-01-15
### Changed
- Updated `pandas`, `dask`, and `numpy` versions.


[1.3.0] 2018-01-15
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
