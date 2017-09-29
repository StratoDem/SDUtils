"""
StratoDem Analytics : sd_config
Principal Author(s) : Michael Clawar
Secondary Author(s) :
Description :

Notes :

September 29, 2017
"""

__all__ = [
    'SDConfig',
]


class SDConfigClass:
    def __init__(self, cpu_count: int=8):
        self._cpu_count = cpu_count
        self.cpu_count = cpu_count

    @property
    def cpu_count(self) -> int:
        return self._cpu_count

    @cpu_count.setter
    def cpu_count(self, cpu_count: int) -> None:
        assert isinstance(cpu_count, int) and cpu_count > 0

        self._cpu_count = cpu_count


SDConfig = SDConfigClass()