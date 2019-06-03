import json
import os
import time

from config.settings import OUTPUT_PATH
from html_util import get_table_content
from util.util import get_content


class Client:
    def __init__(self, proxies, output, marks="ipv6"):
        self.proxies = proxies
        self.output = output
        self.marks = marks
        self.baseurl = 'http://v6directory.twnic.net.tw/directory.cgi?more={0}'

    def get_one_page(self, page):
        page = str(page * 100)
        url = self.baseurl.format(page)
        content = get_content(url, proxy=self.proxies)
        return get_table_content(content.table)

    def get_pages(self, max):
        for x in range(1, max):
            result = self.get_one_page(x)
            print('{0} 正在爬取^^'.format(x))
            self.save(result, self.output)

    def save(self, result, output):
        dir_path = OUTPUT_PATH + '/' + self.marks + '/'
        path = dir_path + self.marks + "_results.jsonl"
        if output == 'jsonl':
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            f = open(path, 'a')
            f.write(json.dumps(result) + '\n')
            f.close()
        else:
            pass


if __name__ == "__main__":
    proxies = {
        "http": "http://127.0.0.1:8123",
        "https": "https://127.0.0.1:8123"
    }
    client = Client(proxies, output='jsonl')
    client.get_pages(121)
