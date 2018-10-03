from ezretry.core import RetryParamItem, __retry_internal, check_params
import logging
import functools

_default_logger = logging.getLogger(__name__)


def retry(retry_params_list=[RetryParamItem()], logger=_default_logger):
    """
    use retry by decorator
    :param retry_params_list: retry exception params
    :param logger: print retry logs
    :return: function
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


def retry_call(func, f_args=None, f_kwargs=None, retry_params_list=[RetryParamItem()], logger=_default_logger):
    """
    this equal below usage:
        @decorator(retry_params_list, logger)
        def func(*f_args, **f_kwargs):
            pass
    """
    check_params(retry_params_list)

    args = f_args if f_args else list()
    kwargs = f_kwargs if f_kwargs else dict()
    return __retry_internal(functools.partial(func, *args, **kwargs), retry_params_list, logger)
