import json
import re

import requests
from bs4 import BeautifulSoup

"""
 从wikileaks中下载指定文件，入口函数为
 `get_all_pages(pages, query_email)`
 前面是需要爬取的页数， 后面是指定查询的语句
 例如， 爬取`arron@email.com`前121页内容，
 输入 `get_all_pages(121, "arron@hbgary.com")

"""
__index = 0


def is_valid(content):
    return True if content.status_code == 200 else False


def get_html(url, proxy=None):
    """
    :param proxy: 代理
    :param url: 爬取的网址参数，先将爬的内容缓存起来
    :return: 返回一个soup类型
    """
    if proxy is None:
        content = requests.get(url=url, headers={'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT '
                                                               '6.3; Win64; x64)'})
        content = content.content
    else:
        # todo: 考虑代理失效的情况
        content = requests.get(url=url, proxies=proxy, headers={'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; '
                                                                              'Windows NT '
                                                                              '6.3; Win64; x64)'})
        if is_valid(content):
            content = content.content
        else:
            content = "error"
    return content


def get_content(url, proxy=None):
    content = get_html(url, proxy=proxy)
    return BeautifulSoup(content, 'lxml')


proxies = {
    "http": "http://127.0.0.1:8123",
    "https": "https://127.0.0.1:8123"
}

# proxies = None

base_url = "https://wikileaks.org/hbgary-emails/"


def get_file_name(content):
    reg_file = r'.*?filename="(.*?)"$'
    k = re.match(reg_file, content)
    return k.group(1)


def save_file(path, content):
    with open(path, "wb") as f:
        f.write(content)


def source_file(content, results):
    try:
        """
        文件下载
        """
        attachment = content.select("ul.attachments")[0].li
        href = attachment.a.get('href')
        results["attachment"] = "https://wikileaks.org" + href
        results = download_by_url(results["attachment"], results)
    except IndexError:
        return results
    finally:
        return results


def download_by_url(url):
    download_file = requests.get(url, proxies=proxies)
    filename = get_file_name(download_file.headers["Content-Disposition"])
    path = "data/" + str(__index) + "-" + filename
    print("{0} 文件正在下载...".format(filename))
    save_file(path, download_file.content)


def get_one_email(url):
    """
    解析一个邮件内部的内容
    :param url:
    :return:
    """
    content = get_content(url, proxy=proxies)

    source = g_source(content)
    download_by_url('https://wikileaks.org'+source)


def g_source(content):
    try:
        source = content.select('p.raw-source')[0].a.get('href')
    except:
        source = None
    return source


def get_body(url):
    content = get_content(url, proxy=proxies)
    tbody = content.select('table.search-result')[0].tbody
    trs = tbody.find_all('tr')
    return [tr.a.get('href') for tr in trs]


def write_file(f, w):
    f.write(json.dumps(w) + '\n')


def one_page_helper(page, from_email):
    search_url = "https://wikileaks.org/hbgary-emails/?q=&mfrom={1}&page={0}&#searchresult"
    url = search_url.format(page, from_email)
    print(url)
    target_urls = get_body(url)
    f = open('./{0}.jsonl'.format(from_email), 'a')
    [write_file(f, get_one_email(base_url + url)) for url in target_urls]


def get_all_pages(pages, from_email):
    for x in range(96, pages):
        print("{0} pages 正在爬取..\n".format(x))
        one_page_helper(x, from_email)


if __name__ == '__main__':
    get_all_pages(121, "aaron@hbgary.com")
