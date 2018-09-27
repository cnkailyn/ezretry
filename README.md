# ezretry
normally retry tools, but we can provide a function to call before next try.

## install
pip install ezretry

## usage
```
from core import retry, RetryParameters


test_index = 100


def change_index():
    global test_index
    test_index -= 1


exception_params = [
    RetryParameters(exceptions=(IndexError,), do=change_index, tries=3, delay=0.1, max_delay=5, back_off=1, jitter=1),
]


@retry(exception_params)
def test_func():
    a = [1, 2, 3]
    global test_index
    return a[test_index]


test_func()
   
```
