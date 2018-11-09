"""
StratoDem Analytics : sd_config
Principal Author(s) : Michael Clawar
Secondary Author(s) :
Description :

Notes :

September 29, 2017
"""

from typing import Optional


__all__ = [
    'SDConfig',
]


class SDConfigClass:
    def __init__(self, cpu_count: int=8, npartitions: int=8, slack_api_token: Optional[str]=None,
                 slack_channel: Optional[str]=None, slack_personal_prefix: Optional[str]=None):
        self._cpu_count = cpu_count
        self.cpu_count = cpu_count
        self._npartitions = npartitions
        self.npartitions = npartitions
        self._slack_api_token = slack_api_token
        self._slack_channel = slack_channel
        self._slack_personal_prefix = slack_personal_prefix

    @property
    def cpu_count(self) -> int:
        return self._cpu_count

    @cpu_count.setter
    def cpu_count(self, cpu_count: int) -> None:
        assert isinstance(cpu_count, int) and cpu_count > 0

        self._cpu_count = cpu_count

    @property
    def npartitions(self) -> int:
        return self._npartitions

    @npartitions.setter
    def npartitions(self, npartitions: int) -> None:
        assert isinstance(npartitions, int) and npartitions > 0

        self._npartitions = npartitions

    @property
    def slack_api_token(self) -> str:
        return self._slack_api_token

    @slack_api_token.setter
    def slack_api_token(self, slack_api_token: str) -> None:
        assert isinstance(slack_api_token, str)

        self._slack_api_token = slack_api_token

    @property
    def slack_channel(self) -> str:
        return self._slack_channel

    @slack_channel.setter
    def slack_channel(self, slack_channel: str) -> None:
        assert isinstance(slack_channel, str)

        self._slack_channel = slack_channel

    @property
    def slack_personal_prefix(self) -> str:
        return self._slack_personal_prefix

    @slack_personal_prefix.setter
    def slack_personal_prefix(self, slack_personal_prefix: str) -> None:
        assert isinstance(slack_personal_prefix, str)

        self._slack_personal_prefix = slack_personal_prefix


SDConfig = SDConfigClass()
