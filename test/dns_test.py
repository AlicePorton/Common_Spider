import asyncio
import re

import aiodns
import requests
from aiohttp import ClientTimeout, ClientSession

import components.fofa_sdk.client as client
import components.virustotal.client as v_client
from components.nslookup.client import dns_query
from config import secure
from util.color import R, Y, W
from util.data_util import DataUtil
from util.file_util import FileUtil
# from util.http_util import HttpUtil

headers = {'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)'}
proxy = "http://127.0.0.1:8123"
# proxy = None
timeout = ClientTimeout(total=10)

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
        if url not in results:
            test = results[url] = {}
        test = results[url]

        async with ClientSession() as session:
            try:
                async with session.get('http://' + url, headers=headers, proxy=proxy, timeout=timeout) as response:
                    content = await response.text()
                    test['title'] = HttpUtil.get_title(content)
            except:
                warning('the {0} 网站主题为空'.format(url))
                test['title'] = 'None'
                pass

loop = asyncio.get_event_loop()
resolver = aiodns.DNSResolver(loop=loop)
test = ["qq.com", "baidu.com", "google.com", "163.com"]
all_results = {}
fofa_client = client.Client(secure.EMAIL, secure.KEY)
vt_client = v_client.Client(secure.VT_KEY)


def warning(*args, **kwargs):
    print('%sWARNING: %s' % (Y, W), end='')
    print(*args, **kwargs)


async def query(name, query_type, _name=""):
    """
    调用nslookup命令解析域名，将结果保存在results中
    :param _name:
    :param name: 应该传入（url, title)二元组
    :param query_type: dns解析类型
    :return:
    """
    lines = name.replace('\n', '').split(' ')
    name = lines[0]
    if name not in all_results:
        test = all_results[name] = {}
    test = all_results[name]
    test["name"] = _name
    try:
        result = await resolver.query(name, query_type)
        if query_type is 'CNAME':
            if 'cname' not in result:
                test['cname'] = result.cname
            else:
                test['cname'] = 'None'
        if query_type is 'A':
            for x in result:
                if 'ips' not in test:
                    test['ips'] = ''
                test['ips'] = (test['ips'] + ',' + x.host)[1:]
            # fixme: 异常检测
            ports = fofa_client.get_port_by_ip(result[0].host)
            test['ports'] = ports
    except:
        warning('the {0} {1} 记录查询为空'.format(name, query_type))
        if query_type is 'A':
            test['ports'] = 'None'
            test['ips'] = 'None'
        all_results[name][query_type.lower()] = 'None'


tasks = []


def write_to_excel(obj, excfile):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    a = 1
    cols = ["子域名", "名称", "IP", "主题", "cname记录", "端口"]
    ws.append(cols)  # 标题
    for k in obj:
        if obj[k] is None:
            continue
        item = obj[k]
        for x in item:
            rowdata = [k, x['name'], x['ip'], x['title'], x['cname'], x['ports']]
            ws.append(rowdata)
        # ws.append(cols) # 标题
    wb.save('../out/' + excfile + '.xlsx')  # 保存
    print('保存路径为 %sout/%s.xlsx' % (R, excfile))


def run(tests, type, _name):
    for i in tests:
        task = asyncio.ensure_future(query(i, type, _name))
        tasks.append(task)
        # t2 = loop.run_until_complete(query(i, 'CNAME'))
        # print(t2)


def append_tasks(func, tasks, iters, **kwargs):
    for i in iters:
        task = asyncio.ensure_future(func(i, **kwargs))
        tasks.append(task)


if __name__ == '__main__':
    tests = FileUtil.get_domains_from_file(file="test.txt")
    # 子域名数据获取
    test = vt_client.get_subdomains(tests)

    # 获取子域名的CNAME A title PORT信息
    for domain in test:
        # tests = test[domain]
        tests = ['www.baidu.com']
        append_tasks(query, tasks=tasks, iters=tests, query_type='CNAME', _name=domain)
        append_tasks(query, tasks=tasks, iters=tests, query_type='A', _name=domain)
        append_tasks(HttpUtil.asnyc_get_title, tasks=tasks, iters=tests, results=all_results)
    loop.run_until_complete(asyncio.wait(tasks))
    print('-----------------')
    print(all_results)
    print('数据爬取完毕，正在保存中 ...')

    for x in all_results:
        all_results[x] = DataUtil.format_by_ip(all_results[x])
    write_to_excel(all_results, 'test')
    loop.close()

