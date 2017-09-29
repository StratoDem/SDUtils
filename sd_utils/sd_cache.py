"""
StratoDem Analytics : sd_cache
Principal Author(s) : Michael Clawar
Secondary Author(s) :
Description :

Notes :

September 29, 2017
"""

import functools


__all__ = [
    'cache',
]


cache = functools.lru_cache(maxsize=1024)
