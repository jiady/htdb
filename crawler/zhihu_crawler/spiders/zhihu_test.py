# -*- coding: utf-8 -*-

import zhihu
import unittest
import scrapy
import os
# usage like below must set PythonPath
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
        name = person.xpath("@title").extract_first(default='not-found')
        href = person.xpath("@href").extract_first(default='not-found')
        hash = href.split('/')[-1]
        self.assertEqual(u"逍遥温温", name);
        self.assertEqual("xiao-yao-wen-wen", hash)

    def test_parse_info(self):
        p = os.path.dirname(os.path.realpath(__file__))
        f = file(p + "/test_data/info.html")
        content = f.read()
        response = scrapy.http.HtmlResponse(url="https://www.zhihu.com/people/jia-dong-yu",
                                            body=content)
        person = items.PersonItem()
        profileCard = response.selector.xpath("//div[@class='zu-main-content-inner']/div[1]")
        person["image_href"] = profileCard.xpath("//img[contains(@class,'Avatar')]/@src").extract_first(
            default='not-found')
        top = profileCard.xpath("//div[@class='top']")
        person["name"] = top.xpath("//span[@class='name']/text()").extract_first(default='not-found')
        person['bio'] = top.xpath("//span[@class='bio']/text()").extract_first(default='not-found')
        infoItem = profileCard.xpath("//div[@class='items']")
        person['city'] = infoItem.xpath("//span[contains(@class,'location')]/@title").extract_first(default='not-found')
        person['gender'] = infoItem.xpath("//span[contains(@class,'gender')]/i/@class").extract_first(
            default='not-found')
        person['school'] = infoItem.xpath("//span[contains(@class,'education')]/@title").extract_first(
            default='not-found')
        person['major'] = infoItem.xpath("//span[contains(@class,'education-extra')]/@title").extract_first(
            default='not-found')
        person['introduction'] = profileCard.xpath("//span[@class='content']/text()").extract_first(default='not-found')
        person['agree_num'] = profileCard.xpath(
            "div[2]//span[@class='zm-profile-header-user-agree']/strong/text()").extract_first(default='not-found')
        sideBar = response.selector.xpath("//div[@class='zu-main-sidebar']/div[1]")
        person['followee_num'] = sideBar.xpath("a[1]/strong/text()").extract_first(default='not-found')
        person['follower_num'] = sideBar.xpath("a[2]/strong/text()").extract_first(default='not-found')
        for key, value in person.items():
            self.assertNotEqual(value, 'not-found')

    def test_item_to_json(self):
        relationItem = items.RelationItem()
        relationItem["follower"] = "a"
        relationItem["followee"] = "b"
        self.assertEqual(str(relationItem),
                         "{'followee': 'b', 'follower': 'a'}")


if __name__ == '__main__':
    unittest.main()
