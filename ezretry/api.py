from ezretry.core import RetryParameters, __retry_internal, check_params
import logging
import functools

_default_logger = logging.getLogger(__name__)


def decorator_retry(retry_params_list=[RetryParameters()], logger=_default_logger):
    """
    retry for exception
    :param retry_params_list:
    :param logger:
    :return:
    """
    check_params(retry_params_list)

    def _inline(func):
        @functools.wraps(func)
        def __inline(*args, **kwargs):
            args = args if args else list()
            kwargs = kwargs if kwargs else dict()
            return __retry_internal(functools.partial(func, *args, **kwargs), retry_params_list, logger)

        return __inline

    return _inline


def retry_call(func, f_args=None, f_kwargs=None, retry_params_list=[RetryParameters()], logger=_default_logger):
    """
    Calls a function and re-executes it if it failed.
    """
    check_params(retry_params_list)

    args = f_args if f_args else list()
    kwargs = f_kwargs if f_kwargs else dict()
    return __retry_internal(functools.partial(func, *args, **kwargs), retry_params_list, logger)


class EzRetryBlock(object):
    """
    Usage for context manager
    """
    def __init__(self, retry_params_list=[RetryParameters()], logger=_default_logger):
        check_params(retry_params_list)
        self.retry_params_list = retry_params_list
        self.logger = logger

    def __enter__(self):
        print("enter")
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exist")
        pass

