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
from typing import Callable, Any, Optional, List, Union

from slackclient import SlackClient

from sd_utils.sd_config import SDConfig


__all__ = ['SDLog', 'log', 'log_func', 'log_gen']


class SDLog:
    contexts = []  # type: List[SDLog]
    # /// #
    set_timer = True
    # /// #
    special_char = '·'
    break_char = '|'

    def __init__(self, message: str='', timer: Optional[bool]=None, slack: bool=False,
                 block: bool=False, max_expected_time: Optional[Union[int, float]]=None) -> None:
        """
        SDLog which logs context on entrance and exit

        Parameters
        ----------
        message: str
            Message to log on both entrance and exit
        timer: bool
            Track time during SDLog context?
        slack: bool
            Log the output to slack?
        block: bool
        max_expected_time: int or float
            Number of seconds that the function can run without adding a warning during __exit__
        """
        timer = self.set_timer if timer is None else timer
        assert isinstance(message, str)
        assert isinstance(timer, bool)
        assert isinstance(slack, bool)
        assert isinstance(block, bool)
        assert max_expected_time is None or isinstance(max_expected_time, (int, float))

        self.main_msg = message
        self.timer = timer
        self.slack = slack
        self.block = block
        self.max_expected_time = max_expected_time

        self.start_time = None

    def __enter__(self) -> 'SDLog':
        print(self._context_buffer_str(), 'Start: ', self.main_msg, sep='')
        if self.slack:
            print(self._context_buffer_str(), '[ Slack ]', sep='')

        self.contexts.append(self)
        self.start_time = time.time()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.contexts.pop()

        if self.timer:
            buffer_str = self._context_buffer_str()
            print(buffer_str, 'End  : ', self.main_msg,
                  ' ', self.time_diff_str, sep='')
            if self.max_expected_time is not None and self.time_diff > self.max_expected_time:
                print(buffer_str, 'SLOW FUNCTION : ', self.main_msg, ' took longer than ',
                      self.max_expected_time, 's!', sep='')
        else:
            print(self._context_buffer_str(), 'End  : ', self.main_msg, sep='')

        if self.slack:
            if SDConfig.slack_api_token is not None and len(SDConfig.slack_api_token) > 0:
                slack_client = SlackClient(SDConfig.slack_api_token)

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
                    channel='#{channel}'.format(channel=SDConfig.slack_channel),
                    text='{prefix} {msg}'.format(prefix=SDConfig.slack_personal_prefix, msg=msg),
                    as_user=True)

    def log(self, *args, show_time: Optional[bool]=None) -> None:
        show_time = self.set_timer if show_time is None else show_time
        assert isinstance(show_time, bool)

        msg = self._format_msg_from_args(*args)

        if show_time:
            print(self._context_buffer_str(), '[ ', msg, ' ] ', self.time_diff_str, sep='')
        else:
            print(self._context_buffer_str(), '[ ', msg, ' ]', sep='')

    @classmethod
    def quick_log(cls, *args) -> None:
        msg = cls._format_msg_from_args(*args)
        now = datetime.datetime.now()
        end_str = ' ] [{:2d}:{:2d}:{:2d}]'.format(now.hour, now.minute, now.second)
        print(cls._context_buffer_str(), '[ ', msg, end_str, sep='')

    # /// Internal only /// #
    @property
    def time_diff(self) -> float:
        return time.time() - self.start_time

    @property
    def time_diff_str(self) -> str:
        now = datetime.datetime.now()
        return '[{:.2f}s] [{:2d}:{:2d}:{:2d}]'.format(
            self.time_diff, now.hour, now.minute, now.second)

    @classmethod
    def _format_msg_from_args(cls, *args) -> str:
        msg = ' '.join(str(x) for x in args).replace('\n', '\n' + cls._context_buffer_str() + '  ')
        return msg

    @classmethod
    def _context_buffer_str(cls) -> str:
        num_contexts = len(cls.contexts)

        group_str = cls.special_char * 3 + cls.break_char
        return str(group_str * (num_contexts // 4) + cls.special_char * (num_contexts % 4))


def log(*args) -> None:
    SDLog.quick_log(*args)


def log_func(func: Optional[Callable]=None,
             max_expected_time: Optional[Union[int, float]]=None) -> Callable[[Any], Any]:
    # If max_expected_time was passed in, then func will be none and we have to return
    # log_func as a partial function with max_expected_time already filled in, to be used as
    # the decorator again
    if func is None:
        return functools.partial(log_func, max_expected_time=max_expected_time)

    assert callable(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Callable[[Any], Any]:
        if 'sdlog' in kwargs:
            sdlog = kwargs.pop('sdlog')
            assert isinstance(sdlog, bool)

            if not sdlog:
                return func(*args, **kwargs)

        with SDLog(func.__qualname__, max_expected_time=max_expected_time):
            return func(*args, **kwargs)
    return wrapper


def log_gen(obj: Any, msg: str) -> Any:
    assert isinstance(msg, str)
    log(msg)
    return obj


if __name__ == '__main__':
    @log_func(max_expected_time=1)
    def test_func():
        time.sleep(2)

    @log_func(max_expected_time=2.3)
    def test_func2():
        time.sleep(1)

    @log_func
    def test_func3():
        time.sleep(2)

    test_func()
    test_func2()
    test_func3()
