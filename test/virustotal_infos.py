import json
import logging
import os
import re
import time
import requests
from selenium import webdriver

from util.html_util import is_valid
from util.util import write_file_content, get_file_content


# 无法封装成功
def get_json(url, proxy=None):
    """
    爬取json类格式的网页
    :param url:
    :param proxy:
    :return: json格式的数据
    """
    headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Language': 'en-US,en;q=0.8',
              'Accept-Encoding': 'gzip',
          }

    session = requests.Session()

    out_time = time.strftime("%Y%m", time.localtime())
    path = 'temp/json/' + url + '-' + out_time + ".json"
    if not os.path.isfile(path):
        logging.info('the %s is not exist' % url)
        if proxy is None:
            content = session.get(url, headers=headers)
            print(content)
        else:
            # todo: 考虑代理失效的情况
            content = requests.get(url=url, proxies=proxy, headers={'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; '
                                                                                  'Windows NT '
                                                                                  '6.3; Win64; x64)'})

            if is_valid(content):
                logging.info('%s SUCCESS' % url)
                content = json.loads(content.content, encoding='utf-8')
            else:
                logging.warning('%s ERROR %s' % (url, content.status_code))
                return 'error'
        print(content)
        write_file_content(path, json.dumps(content))
        return content
    else:
        return json.loads(get_file_content(path))


def test_rw_json():
    k = [{"gg": "gg"}]

    write_file_content("test.json", json.dumps(k).encode())

headers =  {
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Language': 'en-US,en;q=0.8',
              'Content-Type': 'application/json;charset=UTF-8',
          }
cookies = dict(__Cfduid='d905ba28ad8e08462b4858296ebcbb5c61552550108', cf_clearance='ed8349139a9504bc0bc82d45f75bb287ae3b1eae-1552867775-14400-150')
url = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=baidu.com'
res = requests.Session().get(url=url, headers=headers, timeout=25)

print(res)

