# -*- coding: utf-8 -*-

import zhihu
import unittest
import scrapy
import os
#usage like below must set PythonPath
from zhihu_crawler import items


class ZhihuTest(unittest.TestCase):
    def setUp(self):
        self.zhihuSpider = zhihu.ZhihuSpider()

    def test_get_user_account(self):
        t = self.zhihuSpider.loadUserAccount();
        self.assertTrue("email" in t);

    def test_decode(self):
        message = '''"\u767b\u5f55\u6210\u529f"'''
        sub = u"成功"
        message = message.decode("unicode_escape")
        self.assertTrue(sub in message)

    def test_parse_follower(self):
        p = os.path.dirname(os.path.realpath(__file__))
        f = file(p + "/test_data/followee.html")
        content = f.read()
        response = scrapy.http.HtmlResponse(url="https://www.zhihu.com/people/jia-dong-yu/followees",
                                            body=content)
        people = response.selector.xpath("//h2[@class='zm-list-content-title']/a")
        self.assertTrue(len(people) == 20)
        person = people[0]
        name = person.xpath("@title").extract()[0]
        href = person.xpath("@href").extract()[0]
        hash = href.split('/')[-1]
        self.assertEqual(u"逍遥温温", name);
        self.assertEqual("xiao-yao-wen-wen", hash)

    def test_item_to_json(self):
        relationItem = items.RelationItem()
        relationItem["follower"] = "a"
        relationItem["followee"] = "b"
        self.assertEqual(str(relationItem),
                         "{'followee': 'b', 'follower': 'a'}")


if __name__ == '__main__':
    unittest.main()
