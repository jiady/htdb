# -*- coding: utf-8 -*-

import zhihu
import unittest
import scrapy
import os
import json
from scrapy import Selector
from urllib import unquote
# usage like below must set PythonPath
from crawler import items


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
        message = u'\u4e0a\u6d77'
        self.assertEqual(message, u"上海")
        school_target = [u"复旦大学", u"华东师范大学", u"上海交通大学", u"同济大学"]
        self.assertTrue(u'\u4e0a\u6d77\u4ea4\u901a\u5927\u5b66' in school_target)

    def test_parse_follower_more(self):
        p = os.path.dirname(os.path.realpath(__file__))
        f = file(p + "/test_data/followee_next.html")
        content = f.read()
        request = scrapy.http.Request(url="http://zhihu.com", headers={'tracking_user_hash': "22"})
        response = scrapy.http.HtmlResponse(url="https://www.zhihu.com/people/jia-dong-yu/followees",
                                            body=content,
                                            request=request)
        for p in self.zhihuSpider.parse_people_list_more(response):
            self.assertEqual(p['follower'], '22')
            self.assertEqual(p['followee'], 'xiang-zhao-kun')
            break

    def test_parse_info(self):
        p = os.path.dirname(os.path.realpath(__file__))
        f = file(p + "/test_data/info.html")
        content = f.read()

        response = scrapy.http.HtmlResponse(url="https://www.zhihu.com/people/jia-dong-yu",
                                            body=content)
        for person in self.zhihuSpider.parse_people_info(response):
            for key, value in person.items():
                self.assertNotEqual(value, 'not-found')
            self.assertEqual(person['url_name'], 'jia-dong-yu')
            print person['image_href']
            break

    def test_item_to_json(self):
        relationItem = items.RelationItem()
        relationItem["follower"] = "a"
        relationItem["followee"] = "b"
        self.assertEqual(str(relationItem),
                         "{'followee': 'b', 'follower': 'a'}")


if __name__ == '__main__':
    unittest.main()
