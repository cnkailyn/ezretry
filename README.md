# ezretry
normally retry tools, but we can provide a function to call before next try.

## install
pip install ezretry

## usage
```
from ezretry.core import RetryParameters, retry


PROXY = {}

def do_while_exception():
    global PROXY
    PROXY = {
        "http": "http://axbix.com"
    }

except_params = [
    RetryParameters(exceptions=(Exception,), do=do_while_exception, tries=10, delay=1),
]
@retry()
def test_func(except_params):
    raise Exception("test")
   
```
