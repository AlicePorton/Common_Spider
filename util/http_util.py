import asyncio

import requests
from aiohttp import ClientSession

class HttpUtil:
    @staticmethod
    def check(url, timeout=5, **kwargs):
        status = 'N/A'
        try:
            r = requests.get(url, timeout=timeout, **kwargs)
            status = str(r.status_code)
        except requests.exceptions.ConnectTimeout:
            status = "connectTimeout"
        except requests.exceptions.ProxyError:
            status = "ProxyError"
        except requests.exceptions.ConnectionError:
            status = "DOWN"
        except requests.exceptions.HTTPError:
            status = "HttpError"
        except requests.exceptions.ReadTimeout:
            status = "ReadTimeout"
        except requests.exceptions.Timeout:
            status = "TimeoutError"
        except requests.exceptions.TooManyRedirects:
            status = "TooManyRedirects"
        except requests.exceptions.MissingSchema:
            status = "MissingSchema"
        except requests.exceptions.InvalidURL:
            status = "InvalidURL"
        except requests.exceptions.InvalidHeader:
            status = "InvalidHeader"
        except requests.exceptions.URLRequired:
            status = "URLmissing"
        except requests.exceptions.RetryError:
            status = "RetryError"
        except requests.exceptions.InvalidSchema:
            status = "InvalidSchema"
        return status

    @staticmethod
    async def async_check(url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                print('check the url {0}'.format(url))
                status = response.status
                res = await response.read()
                if status is 200:
                    print('url {0} GREEN'.format(url))
                else:
                    print('url {0} RED'.format(url))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(HttpUtil.async_check('http://www.baidu.com'))
    # python3 可以使用asyncio来实现
    # import threading
    #
    #
    # def go_threading(nums, urls):
    #     global interesting
    #     interesting = []
    #     threads = []
    #     for i in nums:
    #         t = threading.Thread(target=HttpUtil.check, args=(urls[i]))
    #         threads.append(t)
    #     for i in nums:
    #         threads[i].start()
    #     for i in nums:
    #         threads[i].join()
    #     print('\n\033[1;32m[DONE..]')
    #
    #
    # go_threading(range(1), ['http://www.baidu.com'])
