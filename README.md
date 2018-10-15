# ezretry
normally retry tools, but we can provide a function to call before next try.

## install
pip install ezretry

## usage
```
"""
this example is for web spider when it need proxy.
"""

import ezretry
import requests

Proxy = {}


class InValidProxy(Exception):
    def __init__(self, msg="proxy is invalid"):
        self.msg = msg

    def __str__(self):
        return self.msg


def refresh_proxy():
    global Proxy
    # this proxy is provided by github https://github.com/jhao104/proxy_pool, just for test.
    ip_port = requests.get("http://123.207.35.36:5010/get").text.strip()
    Proxy = {
        "http": ip_port,
        "https": ip_port
    }
    print(Proxy)


@ezretry.retry(retry_groups=[
    ezretry.RetryGroup(es=(ConnectionError, InValidProxy), do=refresh_proxy, fail_return="我尽力了", tries=2),
    ezretry.RetryGroup(es=(Exception,), do=refresh_proxy, fail_return="我尽力了", tries=2)
])
def get_lago_data(key, page=1):
    global Proxy
    params = {
        "pn": page,
        "kd": key
    }
    data = requests.post("https://www.lagou.com/jobs/positionAjax.json?city=成都&needAddtionalResult=false",
                         data=params, proxies=Proxy, timeout=5).json()
    if "操作太频繁" in data['msg']:
        raise InValidProxy()
    result = data['content']['positionResult']['result']
    return result


def get_lago_data_test(key, page=1):
    global Proxy
    params = {
        "pn": page,
        "kd": key
    }
    data = requests.post("https://www.lagou.com/jobs/positionAjax.json?city=成都&needAddtionalResult=false",
                         data=params, proxies=Proxy, timeout=5).json()
    if "操作太频繁" in data['msg']:
        raise InValidProxy()
    result = data['content']['positionResult']['result']
    return result


for i in range(1):
    print(get_lago_data("Python", i))

for i in range(1):
    print(ezretry.retry_call(get_lago_data_test, f_args=("Python", i), retry_groups=[
        ezretry.RetryGroup(es=(ConnectionError, InValidProxy), do=refresh_proxy, fail_return="我尽力了", tries=2),
        ezretry.RetryGroup(es=(Exception,), do=refresh_proxy, fail_return="我尽力了", tries=2)
        ]))
```
