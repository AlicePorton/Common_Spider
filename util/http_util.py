import asyncio
import re

import requests
from aiohttp import ClientSession

headers = {'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)'}
proxy = "http://127.0.0.1:8123"


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

    @staticmethod
    def get_title(content):
        title = r'<title>(.*?)</title>'
        result = re.search(title, content)
        if result is not None:
            return result.group(1)
        return 'None'

    @staticmethod
    async def asnyc_get_title(url, results):
        url = url.replace('\n', '').split(' ')[0]
        async with ClientSession() as session:
            try:
                async with session.get('http://' + url, headers=headers, proxy=proxy) as response:
                    content = await response.text()
                    if url not in results:
                        test = results[url] = {}
                    test = results[url]
                    test['title'] = HttpUtil.get_title(content)
            except:
                pass
