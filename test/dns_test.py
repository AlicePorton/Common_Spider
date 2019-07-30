import asyncio

import aiodns

import components.fofa_sdk.client as client
from components.nslookup.client import dns_query
from config import secure
from util.color import R
from util.data_util import DataUtil
from util.file_util import FileUtil
from util.http_util import HttpUtil

loop = asyncio.get_event_loop()
resolver = aiodns.DNSResolver(loop=loop)
test = ["qq.com", "baidu.com", "google.com", "163.com"]
all_results = {}
fofa_client = client.Client(secure.EMAIL, secure.KEY)


async def query(name, query_type):
    lines = name.replace('\n', '').split(' ')
    name = lines[0]
    _title = lines[1]
    if name not in all_results:
        test = all_results[name] = {}
    test = all_results[name]
    test["name"] = _title
    try:
        result = await resolver.query(name, query_type)
        if query_type is 'CNAME':
            if 'cname' not in result:
                test['cname'] = result.cname
            else:
                test['cname'] = 'None'
        if query_type is 'A':
            print(result)
            for x in result:
                if 'ips' not in test:
                    test['ips'] = ''
                test['ips'] = (test['ips'] + ',' + x.host)[1:]
            # fixme: 异常检测
            ports = fofa_client.get_port_by_ip(result[0].host)
            test['ports'] = ports
    except:
        print('the name {0} is in Error, delete it'.format(name))
        all_results[name][query_type.lower()] = 'None'


tasks = []


def write_to_excel(obj, excfile):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    a = 1
    cols = ["子域名", "名称",  "IP", "主题", "cname记录", "端口"]
    ws.append(cols)  # 标题
    for k in obj:
        if obj[k] is None:
            continue
        item = obj[k]
        for x in item:
            rowdata = [k, x['name'], x['ip'], x['title'], x['cname'], x['ports']]
            ws.append(rowdata)
        # ws.append(cols) # 标题
    print('保存中')
    wb.save('../out/' + excfile + '.xlsx')  # 保存
    print('%s保存路径为 out/%s.xlsx' % (R, excfile))


def run(tests, type):
    for i in tests:
        task = asyncio.ensure_future(query(i, type))
        tasks.append(task)
        # t2 = loop.run_until_complete(query(i, 'CNAME'))
        # print(t2)


def append_tasks(func, tasks, iters, **kwargs):
    for i in iters:
        task = asyncio.ensure_future(func(i, **kwargs))
        tasks.append(task)


if __name__ == '__main__':
    tests = FileUtil.get_domains_from_file(file="test.txt")
    append_tasks(query, tasks=tasks, iters=tests, query_type='CNAME')
    append_tasks(query, tasks=tasks, iters=tests, query_type='A')
    append_tasks(HttpUtil.asnyc_get_title, tasks=tasks, iters=tests, results=all_results)
    loop.run_until_complete(asyncio.wait(tasks))
    print('-----------------')
    print(all_results)

    for x in all_results:
        all_results[x] = DataUtil.format_by_ip(all_results[x])
    write_to_excel(all_results, 'test')
    loop.close()
# print(dns_query('baidu.com', 'A'))
# print(dns_query('qq.com', 'A'))
# print(dns_query('google.com', 'A'))

# from components.nslookup.client import dns_query
#
# print(dns_query('baidu.com', 'NS'))
# print(dns_query('www.baidu.com', 'A'))
# print(dns_query('www.a.shifen.com', 'A'))
#
# dns_query('163.com', 'MX')
# print(dns_query('163.com', 'CNAME'))
# print(dns_query('www.uwintech.cn', 'CNAME')[0])
