import asyncio
import sys
import unittest

from aiohttp import ClientSession

import components.fofa_sdk.client as client
from config import secure

sys.path.append('../')

param = {"email": secure.EMAIL, "key": secure.KEY}


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


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = client.Client(secure.EMAIL, secure.KEY)

    def test_get_userinfo(self):
        userinfo = self.client.get_userinfo()
        self.assertIn("isvip", userinfo)

    def test_get_data_normal(self):
        query = """fofa.so"""
        data = self.client.get_data(query_str=query)
        self.assertIn("results", data)
        self.assertIn("page", data)
        self.assertIn("mode", data)

    # def test_async_data(self):
    #     query = """fofa.so"""
    #     t = self.client.async_get_data(query_str=query)
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(t)
    #     loop.close()
    #     print(t)

    def test_get_data_field(self):
        """
        测试返回结果是否在fields范围之内
        :return:
        """
        query = """host = 'fofa.so'"""
        fields = "host, title, port, country"
        data = self.client.get_data(query, fields=fields)
        # TODO: 写入样本数据（只写入一次）
        self.assertIn("results", data)
        self.assertIn("page", data)
        self.assertIn("size", data)
        self.assertIn("mode", data)
        self.assertIn("query", data)

        self.assertEqual(len(data["results"][0]), len(fields.split(',')))

    def test_get_data_by_ip(self):
        query = """120.96.247.52"""
        fields = "host, title, country, port"
        # fields = "port"
        data = self.client.get_data(query, fields=fields, size=10)
        self.assertLessEqual(len(data['results']), 10)
        self.assertIn("results", data)
        self.assertIn("page", data)
        self.assertIn("size", data)
        self.assertIn("mode", data)
        self.assertIn("query", data)
        print(data)

    def test_get_port_by_ip(self):
        query = """120.96.247.52"""
        # fields = "host, title, country, port"
        fields = "port"
        data = self.client.get_port_by_ip(query)
        self.assertLessEqual(len(data.split(',')), 4)
        self.assertIn("443", data)



    def test_get_domain(self):
        data = self.client.get_domains(ip="91.223.115.81")
        self.assertGreater(len(data), 0)
        error_data = self.client.get_domains(ip="12.12.12.12")
        self.assertEqual(error_data, 'No results')

    def test_get_ip_basic(self):
        data = self.client.get_ip_basic(ip="8.8.8.8")
        self.assertGreater(len(data), 0)
        self.assertEqual(len(data["results"][0]), 4)


if __name__ == '__main__':
    unittest.main()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(async_http_get("https://fofa.so/api/v1/info/my", param=param))
    # loop.close()
