# -*- coding: utf-8 -*-
import scrapy
import json
import os
from crawler import items
from scrapy import Selector
import logging
import logging.handlers
from crawler.mail import Mail
from crawler import redis_const
import redis


class filterConditon:
    # propogation node limit condition
    school_target = [u"复旦大学", u"华东师范大学", u"上海交通大学", u"同济大学", u"SJTU", u"sjtu", u"fdu", u"FDU", u"ECNU", u"ecnu",
                     u"上海财经大学", u"上海外国语大学"]
    followee_min = 0
    followee_max = 1000
    # target node limitation
    location_target = u"上海"
    gender_target = "female"
    follower_min = 0
    follower_max = 3000
    # ranking dict
    topic_score = {}


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    base = "http://www.zhihu.com"
    spider_filter = filterConditon()
    headers = {}
    sub_name = ""
    user = ""
    pwd = ""
    QUEUE_NAME = redis_const.QUEUE_PREFIX

    # not add header will lead to getting 500 internal error.
    def __init__(self, user=None, pwd=None, sub_name=None, start_from_redis=False,
                 start_from_file=None):
        if user is None or pwd is None or sub_name is None:
            self.logger.error("an sub_config must be given")
            exit(0)
        self.user = user
        self.pwd = pwd
        self.sub_name = sub_name
        self.start_from_redis = start_from_redis
        self.start_from_file = start_from_file
        self.QUEUE_NAME = redis_const.QUEUE_PREFIX + self.sub_name
        handler = logging.handlers.TimedRotatingFileHandler(
            "htdb_" + self.sub_name + ".log",
            when='D',
            backupCount=7)
        fmt = '%(asctime)s|%(filename)s:%(funcName)s:%(lineno)s:[%(name)s]:%(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        self.flog = logging.getLogger('htdb')
        self.flog.addHandler(handler)
        self.flog.setLevel(logging.DEBUG)
        self.myMail = Mail(self.flog)
        self.headers = {
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'Keep-Alive',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.zhihu.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
        }

    def send_mail(self, subject, text, lock=600):
        self.myMail.send_timed(lock, subject + "@" + self.sub_name, text)

    def loadUserAccount(self):
        form_data_to_post = {
            "email": self.user,
            "password": self.pwd,
            "remember_me": "true"
        }
        self.logger.info(form_data_to_post)
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
        self.headers['X-Xsrftoken'] = xsrf
        yield scrapy.FormRequest(
            "http://www.zhihu.com/login/email",
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )

    def startUrls(self):
        url_head = "https://www.zhihu.com/people/"
        seed_users = ["jia-dong-yu"]
        if self.start_from_redis:
            rclient = redis.StrictRedis(host="localhost", port=6379, db=0)
            seed_users = rclient.smembers(self.QUEUE_NAME)
        if self.start_from_file is not None:
            f = open(self.start_from_file, 'r')
            seed_users = f.readlines()
        ret_list = []
        for user in seed_users:
            ret_list.append(scrapy.Request(url_head + user, headers=self.headers, dont_filter=True,
                                           callback=self.parse_people_info))
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

    def parse_people_list_more(self, response):
        try:
            j = json.loads(response.body)
            sel = Selector(text=" ".join(j['msg']))
            self.logger.info(response.request.headers['tracking_user_hash'])
            follower_hash = response.request.headers['tracking_user_hash']
            people = sel.xpath("//h2[@class='zm-list-content-title']/a")
            for person in people:
                # name = person.xpath("@title").extract_first(default='not-found')
                href = person.xpath("@href").extract_first(default='not-found')
                url_name = href.split('/')[-1]
                ret = items.RelationItem()
                ret["follower"] = follower_hash
                ret["followee"] = url_name
                yield ret
                self.logger.info(href)
                yield scrapy.Request(href, callback=self.parse_people_info, headers=self.headers)
        except Exception, e:
            self.send_mail("parse_people_list_exception", str(e))

    def judge_person_as_valid_source(self, person):
        if person['school'] not in self.spider_filter.school_target:
            return False
        if int(person['followee_num']) < self.spider_filter.followee_min:
            return False
        if int(person['followee_num']) > self.spider_filter.followee_max:
            return False
        return True

    def judge_person_as_target(self, person):
        if (person['school'] not in self.spider_filter.school_target) and person[
            'city'] != self.spider_filter.location_target:
            return False
        if not person['if_female']:
            return False
        if int(person['follower_num']) > self.spider_filter.follower_max:
            return False
        if int(person['follower_num']) < self.spider_filter.follower_min:
            return False
        return True

    def parse_people_info(self, response):
        try:
            person = items.PersonItem()
            profileCard = response.selector.xpath("//div[@class='zu-main-content-inner']/div[1]")
            person["image_href"] = profileCard.xpath(".//img[contains(@class,'Avatar--l')]/@src").extract_first(
                default='not-found')
            person["url_name"] = response.url.split('/')[-1]
            info = response.xpath("//script[@data-name='current_people']/text()").extract_first(
                default="[not-found]")
            basic_info = info[1:-1].split(',')
            person['hash_id'] = basic_info[3].strip('"')
            top = profileCard.xpath(".//div[@class='top']")
            person["name"] = top.xpath(".//span[@class='name']/text()").extract_first(default='not-found')
            person['bio'] = top.xpath(".//span[@class='bio']/text()").extract_first(default='not-found')
            infoItem = profileCard.xpath("//div[@class='items']")
            person['city'] = infoItem.xpath(".//span[contains(@class,'location')]/@title").extract_first(
                default='not-found')
            gender = infoItem.xpath(".//span[contains(@class,'gender')]/i/@class").extract_first(
                default='not-found')
            person['if_female'] = 'female' in gender
            person['school'] = infoItem.xpath(".//span[contains(@class,'education')]/@title").extract_first(
                default='not-found')
            person['major'] = infoItem.xpath(".//span[contains(@class,'education-extra')]/@title").extract_first(
                default='not-found')
            person['introduction'] = profileCard.xpath(".//span[@class='content']/text()").extract_first(
                default='not-found').strip("\n")
            person['agree_num'] = profileCard.xpath(
                ".//div[@class='zm-profile-header-info-list']//span[@class='zm-profile-header-user-agree']/strong/text()").extract_first(
                default='not-found')
            sideBar = response.selector.xpath(".//div[@class='zu-main-sidebar']/div[1]")
            person['followee_num'] = sideBar.xpath("a[1]/strong/text()").extract_first(default='not-found')
            person['follower_num'] = sideBar.xpath("a[2]/strong/text()").extract_first(default='not-found')

            yield person

            if self.judge_person_as_target(person):
                target = items.TargetPersonItem()
                target['hash_id'] = person['hash_id']
                yield target

            if self.judge_person_as_valid_source(person):
                target = items.PropogationPersonItem()
                target['hash_id'] = person['hash_id']
                yield target
                form = dict()
                form["method"] = "next"
                params = dict()
                params['offset'] = 0
                params['order_by'] = "created"
                params['hash_id'] = person['hash_id']
                for offset in xrange(int(person['followee_num']) / 20 + 1):
                    params['offset'] = offset * 20
                    form['params'] = json.dumps(params)
                    self.logger.info(str(form))
                    header_this = self.headers.copy()
                    header_this['Referer'] = response.url + "/followees"
                    header_this['tracking_user_hash'] = person['hash_id']
                    yield scrapy.FormRequest(
                        "https://www.zhihu.com/node/ProfileFolloweesListV2",
                        formdata=form,
                        headers=header_this,
                        callback=self.parse_people_list_more
                    )
        except Exception, e:
            self.send_mail("parse_people_list_exception", str(e))
