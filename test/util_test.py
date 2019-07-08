import util.util as util
import unittest


class UtilTestCase(unittest.TestCase):
    def test_http_check(self):
        status = util.Check.getHttpStatusCode('http://www.baidu.com')
        self.assertEqual(status, 200)
        status_fail = util.Check.getHttpStatusCode('http://fasdfadsf.tw/')
        self.assertNotEqual(status_fail, 200)
