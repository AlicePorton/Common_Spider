# -*- coding: utf-8 -*-
import base64
import json

# from urllib import request
import requests
from aiohttp import ClientSession


def http_get(url, param):
    # param = bytes(param)
    # param = urllib.parse.urlencode(param)
    # url = "%s?%s" % (url, param)
    try:
        req = requests.get(url, params=param)
        res = req.content
        res = str(res, encoding='utf8')
        if "errmsg" in res:
            raise RuntimeError(res)
    #     todo: test the runtime error whether normal
    except RuntimeError as e:
        print("errmsg：", e.content())
        raise e
    return res


async def async_http_get(url, param):
    async with ClientSession() as session:
        try:
            async with session.get(url, params=param) as response:
                res = await response.text()
                print(res)
                if "errmsg" in res:
                    raise RuntimeError(res)
        except:
            pass

class Client:
    """
    通过fofa api爬取数据
    """

    def __init__(self, email, key):
        self.email = email
        self.key = key
        self.base_url = "https://fofa.so"
        self.search_api_url = "/api/v1/search/all"
        self.login_api_url = "/api/v1/info/my"
        self.get_userinfo()  # check email and key

    def get_userinfo(self):
        """
        获取用户信息
        :return:
        """
        api_full_url = "%s%s" % (self.base_url, self.login_api_url)
        param = {"email": self.email, "key": self.key}
        res = http_get(api_full_url, param)
        return json.loads(res)

    def get_data(self, query_str, page=1, fields="", **kwargs):
        res = self.get_json_data(query_str, page, fields, **kwargs)
        return json.loads(res)

    def get_json_data(self, query_str, page=1, fields="", **kwargs):
        api_full_url = "%s%s" % (self.base_url, self.search_api_url)
        query_str = bytes(query_str, encoding="utf8")
        param = {"qbase64": base64.b64encode(query_str), "email": self.email, "key": self.key, "page": page,
                 "fields": fields}
        for key, value in kwargs.items():
            print('{0}:{1}'.format(key, value))
            param[key] = value
        res = http_get(api_full_url, param)

        return res

    async def async_get_json_data(self, query_str, page=1, fields="", **kwargs):
        api_full_url = "%s%s" % (self.base_url, self.search_api_url)
        query_str = bytes(query_str, encoding="utf8")
        param = {"qbase64": base64.b64encode(query_str), "email": self.email, "key": self.key, "page": page,
                 "fields": fields}
        for key, value in kwargs.items():
            print('{0}:{1}'.format(key, value))
            param[key] = value
        res = await async_http_get(api_full_url, param)
        return res

    async def async_get_data(self, query_str, page=1, fields="", **kwargs):
        res = await self.async_get_json_data(query_str, page, fields, **kwargs)
        return json.loads(res)

    def get_domains(self, ip=""):
        query = """ip={0}""".format(ip)
        fileds = "domain"
        raw_domains = self.get_data(query, fields=fileds)["results"]
        domains = list(set([one for one in raw_domains if one is not ""]))
        if not domains:
            return 'No results'
        return domains

    def get_ip_basic(self, ip=""):
        query = """ip={0}""".format(ip)
        fileds = "country_name, province, latitude, longitude"
        raw = self.get_data(query, fields=fileds)
        return raw

    def get_port_by_ip(self, ip=""):
        query="""ip={0}""".format(ip)
        fileds = "port"
        raw = self.get_data(query, fields=fileds)
        ports = set(raw['results'])
        return ",".join(ports)

