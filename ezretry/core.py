"""
core
"""
import time
import random


class RetryException(Exception):

    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg


class RetryGroup(object):
    def __init__(self, es=(Exception,), do=None, fail_return=None, tries=-1,
                 delay=0, max_delay=None, back_off=1, jitter=0):
        """

        :param es: tuple or list of Exceptions
        :param do: the called function before every time retry
        :param fail_return: when arrived the max try times, it will return fail_return
        :param tries: the maximum number of attempts. default: -1 (infinite).
        :param delay: initial delay between attempts. default: 0.
        :param max_delay: the maximum value of delay. default: None (no limit).
        :param back_off: multiplier applied to delay between attempts. default: 1 (no back_off).
        :param jitter: extra seconds added to delay between attempts. default: 0.
                       fixed if a number, random if a range tuple (min, max)
        """
        self.id_name = "-".join(sorted([i.__name__ for i in es]))
        self.exceptions = es
        self.do = do
        self.fail_return = fail_return
        self.tries = tries
        self.delay = delay
        self.max_delay = max_delay
        self.back_off = back_off
        self.jitter = jitter


def __retry_internal(func, retry_params_list, logger):
    """
    Executes a function and retries it if it failed.
    """
    # init try record
    try_record = {}
    for retry_param in retry_params_list:
        try_record.setdefault(retry_param.id_name, {"try": 1, "delay": retry_param.delay})

    while True:
        try:
            return func()
        except Exception as e:
            catch = False
            for item in retry_params_list:
                if isinstance(e, item.exceptions):
                    cur_try_count = try_record[item.id_name]['try']
                    cur_delay = try_record[item.id_name]['delay']
                    if item.tries == -1 or cur_try_count <= item.tries:
                        if logger:
                            logger.warning('retry except "%s" %sth, retrying for next in %s seconds...',
                                           e, cur_try_count, cur_delay)

                        time.sleep(cur_delay)

                        next_delay = cur_delay * item.back_off

                        if isinstance(item.jitter, tuple):
                            next_delay += random.uniform(*item.jitter)
                        else:
                            next_delay += item.jitter
                        if item.max_delay is not None:
                            next_delay = min(next_delay, item.max_delay)

                        if callable(item.do):
                            item.do()
                        try_record[item.id_name]['try'] = cur_try_count + 1
                        try_record[item.id_name]['delay'] = next_delay
                        catch = True
                        break
                    else:
                        if item.fail_return:
                            return item.fail_return

                        raise RetryException("retry caught, but arrived max retry times."
                                             " caused by %s:%s" % (e.__class__.__name__, e))
            if not catch:
                raise


def check_params(retry_params_list):
    if not isinstance(retry_params_list, (list, tuple)):
        raise RetryException("params error, param 'retry_params_list' must be a list or tuple")
    for i in retry_params_list:
        if not isinstance(i, RetryGroup):
            raise RetryException("param 'retry_params_list' object must be the instance of RetryParameters")
