import os
import unittest

from components.tw_IPV6 import client
from config.settings import OUTPUT_PATH


class IPV6ClientTestCase(unittest.TestCase):
    def setUp(self):
        proxies = {
            "http": "http://127.0.0.1:8123",
            "https": "https://127.0.0.1:8123"
        }
        self.client = client.Client(proxies, 'jsonl')

    def test_get_one_page(self):
        result = self.client.get_one_page(1)
        self.assertGreater(len(result), 0)
        case = result[0]
        heads = ["序號", "類別", "所屬單位", "網站名稱", "IPv6位址"]
        [self.assertIn(head, case) for head in heads]

    def test_save_file(self):
        result = self.client.get_one_page(1)
        self.client.save(result, 'jsonl')
        file_path = OUTPUT_PATH + "/ipv6/ipv6_results.jsonl"
        is_exist = os.path.isfile(file_path)
        self.assertTrue(is_exist, 'file is exist')
