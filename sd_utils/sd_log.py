"""
File: sd_log.py

Description: Logging utilities
Principal Author(s): Michael Clawar
Secondary Author(s):

Notes:

December 12, 2016
StratoDem Analytics, LLC
"""

import datetime
import functools
import time
from typing import Callable, Any, Optional, List

from slackclient import SlackClient


__all__ = ['SDLog', 'log', 'log_func', 'log_gen', 'cache']


class SDLog:
    contexts = []  # type: List[SDLog]
    # /// #
    set_timer = True
    # /// #
    special_char = '·'
    break_char = '|'

    def __init__(self, message: str='', timer: Optional[bool]=None, slack: bool=False,
                 block: bool=False,
                 slack_api_token: Optional[str]=None, slack_channel: Optional[str]=None,
                 slack_personal_prefix: Optional[str]=None) -> None:
        timer = self.set_timer if timer is None else timer
        assert isinstance(message, str)
        assert isinstance(timer, bool)
        assert isinstance(slack, bool)
        assert isinstance(block, bool)
        assert slack_api_token is None or isinstance(slack_api_token, str)
        assert slack_channel is None or isinstance(slack_channel, str)
        assert slack_personal_prefix is None or isinstance(slack_personal_prefix, str)

        self.main_msg = message
        self.timer = timer
        self.slack = slack
        self.block = block
        self.slack_api_token = slack_api_token
        self.slack_channel = slack_channel
        self.slack_personal_prefix = slack_personal_prefix

        self.start_time = None

    def __enter__(self) -> 'SDLog':
        print(self.context_buffer_str(), 'Start: ', self.main_msg, sep='')
        if self.slack:
            print(self.context_buffer_str(), '[ Slack ]', sep='')

        self.contexts.append(self)
        self.start_time = time.time()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.contexts.pop()

        if self.timer:
            print(self.context_buffer_str(), 'End  : ', self.main_msg,
                  ' ', self.time_diff_str(), sep='')
        else:
            print(self.context_buffer_str(), 'End  : ', self.main_msg, sep='')

        if self.slack:
            if self.slack_api_token is not None and len(self.slack_api_token) > 0:
                slack_client = SlackClient(self.slack_api_token)

                # if isinstance(exc_type, KeyboardInterrupt):
                #     return

                if exc_type is not None:
                    msg = '*I AM SORRY I BROKE*. `{msg}`, which started at {time} ' \
                          'had this exception:\n```\n{exception} {exception_value}\n```' \
                        .format(msg=self.main_msg,
                                time=time.strftime('%m-%d %H:%M:%S',
                                                   time.localtime(self.start_time)),
                                exception=exc_type,
                                exception_value=exc_val)
                else:
                    msg = '*FINISHED* `{msg}`, which started at {time}. ' \
                          'DID I DO GOOD?? :tada:' \
                        .format(msg=self.main_msg,
                                time=time.strftime('%m-%d %H:%M:%S',
                                                   time.localtime(self.start_time)),
                                exception=exc_type)

                slack_client.api_call(
                    'chat.postMessage',
                    channel='#{channel}'.format(channel=self.slack_channel),
                    text='{prefix} {msg}'.format(prefix=self.slack_personal_prefix, msg=msg),
                    as_user=True)

    def log(self, *args, show_time: Optional[bool]=None) -> None:
        show_time = self.set_timer if show_time is None else show_time
        assert isinstance(show_time, bool)

        msg = self.format_msg_from_args(*args)

        if show_time:
            print(self.context_buffer_str(), '[ ', msg, ' ] ', self.time_diff_str(), sep='')
        else:
            print(self.context_buffer_str(), '[ ', msg, ' ]', sep='')

    @classmethod
    def quick_log(cls, *args) -> None:
        msg = cls.format_msg_from_args(*args)
        now = datetime.datetime.now()
        end_str = ' ] [{:2d}:{:2d}:{:2d}]'.format(now.hour, now.minute, now.second)
        print(cls.context_buffer_str(), '[ ', msg, end_str, sep='')

    # /// Internal only /// #
    def time_diff_str(self) -> str:
        time_diff = time.time() - self.start_time
        now = datetime.datetime.now()
        return '[{:.2f}s] [{:2d}:{:2d}:{:2d}]'.format(time_diff, now.hour, now.minute, now.second)

    @classmethod
    def format_msg_from_args(cls, *args) -> str:
        msg = ' '.join(str(x) for x in args).replace('\n', '\n' + cls.context_buffer_str() + '  ')
        return msg

    @classmethod
    def context_buffer_str(cls) -> str:
        num_contexts = len(cls.contexts)

        group_str = cls.special_char * 3 + cls.break_char
        return str(group_str * (num_contexts // 4) + cls.special_char * (num_contexts % 4))


def log(*args) -> None:
    SDLog.quick_log(*args)


def log_func(func) -> Callable[[Any], Any]:
    """Decorator parameters."""
    assert callable(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Callable[[Any], Any]:
        if 'sdlog' in kwargs:
            sdlog = kwargs.pop('sdlog')
            assert isinstance(sdlog, bool)

            if not sdlog:
                return func(*args, **kwargs)

        with SDLog(func.__qualname__):
            return func(*args, **kwargs)
    return wrapper


def log_gen(obj: Any, msg: str) -> Any:
    assert isinstance(msg, str)
    log(msg)
    return obj
