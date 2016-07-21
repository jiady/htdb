# -*- coding: utf-8 -*-
import scrapy
import json
import os


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    # not add header will lead to getting 500 internal error.
    headers = {
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'Keep-Alive',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.zhihu.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
    }

    def loadUserAccount(self):
        p = os.path.dirname(os.path.realpath(__file__))
        user_account = file(p + '/user_account.private')
        form_data_to_post = json.load(user_account)
        return form_data_to_post

    def start_requests(self):
        yield scrapy.Request(
            "http://www.zhihu.com",
            callback=self.login,
            headers=self.headers
        )

    def login(self, response):
        xsrf = scrapy.Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        self.logger.info("xsrf:%s", xsrf)
        post_data = self.loadUserAccount()
        post_data['_xsrf'] = xsrf
        yield scrapy.FormRequest(
            "http://www.zhihu.com/login/email",
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )

    def startUrls(self):
        url_head = "https://www.zhihu.com/people/"
        url_tails = ["/followees", "/followers"]
        seed_users = ["jia-dong-yu"]
        ret_list = []
        for user in seed_users:
            for url_tail in url_tails:
                ret_list.append(scrapy.Request(url_head + user + url_tail), headers=self.headers,
                                callback=self.parse_people_list)
        return ret_list

    def check_login(self, response):
        if response.status == 200:
            message = response.selector.xpath("//p[1]").extract()[0].decode("unicode_escape")
            if u"成功" in message:
                self.logger.info("login success!!!")
                return self.startUrls()
            else:
                self.logger.error("login failed:%s", message)
        else:
            self.logger.error("response status not 200：%d", response.status)

    def parse_people_list(self, response):
        pass

    def parse_people_list_detail(self,response):
        pass

    def parse_people_info(self, response):
        pass