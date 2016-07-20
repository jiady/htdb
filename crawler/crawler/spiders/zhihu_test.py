import zhihu
import unittest


class ZhihuTest(unittest.TestCase):
    def setUp(self):
        self.zhihuSpider = zhihu.ZhihuSpider()

    def test_get_user_account(self):
        t = self.zhihuSpider.loadUserAccount();
        self.assertTrue("email" in t);


if __name__ == '__main__':
    unittest.main()
