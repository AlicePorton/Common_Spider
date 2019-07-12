import util.util as util
import unittest

from util.http import HttpUtil


class UtilTestCase(unittest.TestCase):
    def test_http_check(self):
        status = HttpUtil.check('http://www.baidu.com')
        self.assertEqual('200', status)
        status_fail = HttpUtil.check('http://fasdfadsf.tw/')
        self.assertNotEqual('200', status_fail)


