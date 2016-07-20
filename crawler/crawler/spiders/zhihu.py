# -*- coding: utf-8 -*-
import scrapy
import json
import os


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
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
        print xsrf
        post_data = self.loadUserAccount()
        post_data['_xsrf'] = xsrf;
        yield scrapy.FormRequest(
            "http://www.zhihu.com/login/email",
            formdata=post_data,
            headers=self.headers,
            callback=self.after_login
        )

    def after_login(self, response):
        print "after_login"
        print response.selector.extract().decode()
        print "leave_after_login"

    def parse(self, response):
        pass
