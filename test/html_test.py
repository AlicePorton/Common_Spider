import asyncio
import re

from aiohttp import ClientSession

import time
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from util.file_util import FileUtil
from util.http_util import HttpUtil


headers = {'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)'}
proxy = "http://127.0.0.1:8123"


async def hello(url):
    async with ClientSession() as session:
        async with session.get('http://' + url, headers=headers, proxy="http://127.0.0.1:8123") as response:
            content = await response.text()
            print(url+'正在获取^')
            print(HttpUtil.get_title(content))


def run(tasks, tests):
    for i in tests:
        task = asyncio.ensure_future(hello(i))
        tasks.append(task)


if __name__ == '__main__':
    tests = FileUtil.get_domains_from_file(file="test.txt")
    tasks = []
    loop = asyncio.get_event_loop()
    run(tasks, tests)
    loop.run_until_complete(asyncio.wait(tasks))
