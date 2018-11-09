# SDUtils
Standard quality of life utilities used across StratoDem Analytics projects.
- Logging
- Type checking for `pandas`, `xarray` and `dask`
- Conversion from `pandas` to `xarray`
- File reading (multiprocessed) into `pandas` and `dask` from various formats
    - Mainly simple wrappers for `pandas.read_*` with standard settings


## Configuring the environment

### Slack for logging
To set up global Slack configuration for, e.g., a data processing pipeline
that logs messages to a Slack channel

```python
from sd_utils.sd_config import SDConfig

SDConfig.slack_api_token = 'my-api-token-here'
SDConfig.slack_channel = 'channel-id-to-post-to'
SDConfig.slack_personal_prefix = 'user-id-to-tag'
```

Anything with `sdu.SDLog(..., slack=True)` will now log the message to the
given Slack channel with an optional user tagged in the message.

```python
with sdu.SDLog('My process', slack=True):
    print('my process')
```

This will log a message to the Slack channel notifying that 'My process' has finished
after starting at the start time.

### Threads and partitions
Increasing the general number of cores to use for multiprocessing
```python
from sd_utils.sd_config import SDConfig

SDConfig.cpu_count = 16     # Use 16 threads
```

Modifying the default number of partitions to use for `dask` computations
```python
from sd_utils.sd_config import SDConfig

SDConfig.npartitions = 25   # Use 25 partitions as the default for dask
```
