import os

import config
from components.nslookup.client import dns_query
from util.color import R, G
from util.data_util import DataUtil
from util.query import Query
from util.util import get_content


# 获取title信息
def get_title(domain):
    url = "http://" + domain
    try:
        content = get_content(url)
        print("正在获取%s主题：" % url)
        print(content.title.string)
        return "".join(content.title.string)

    except:
        return 'None'


def get_ip(domain):
    result = []
    ips = dns_query(domain, 'A')
    if ips is None:
        return 'None'
    for ip in ips:
        if ip.rdtype == 1:
            result.append(ip.to_text())
    return ','.join(result)


def get_cname(domain):
    cname = dns_query(domain, 'CNAME')
    if cname is None:
        return 'None'
    result = []
    try:
        for k in cname:
            result.append(k.to_text()[:-1])
        return ','.join(result)

    except:
        return 'None'


def write_to_excel(obj, excfile):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    a = 1
    cols = ["子域名", "IP", "主题", "cname记录"]
    ws.append(cols)  # 标题
    for k in obj:
        rowdata = [k["domain"], k["ip"], k["title"], k["cname"]]
        ws.append(rowdata)  # 写行
        # ws.append(cols) # 标题
    print('保存中')
    wb.save('../out/' + excfile + '.xlsx')  # 保存
    print('%s保存路径为 out/%s.xlsx' % (R, excfile))


def get_domains_from_file(file=None):
    if file is None:
        return []
    with open(file) as f:
        results = f.readlines()
    return results


def get_all(test='', last='', file=''):
    if test is not '':
        domains = Query().get_sub_domains(domains=[test])
        domains = domains[test]
    if file:
        domains = get_domains_from_file(file=file)
        test = file
    results = []
    for domain in domains:
        domain = domain.replace('\n', '')
        print(domain)
        title = get_title(domain)
        ips = get_ip(domain)
        if ips is 'None':
            continue
        cname = get_cname(domain)
        one = {
            "domain": domain,
            "title": title,
            "ips": ips,
            "cname": cname,
        }
        one = DataUtil.format_by_ip(one)
        results = DataUtil.append(results, one)
    print(results)

    #
    write_to_excel(results, test + last)


if __name__ == '__main__':
    get_all(file='test.txt')
