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
import time
import ConfigParser


def _monkey_patching_HTTPClientParser_statusReceived():
    """
    monkey patching for scrapy.xlib.tx._newclient.HTTPClientParser.statusReceived
    """
    from twisted.web._newclient import HTTPClientParser, ParseError
    old_sr = HTTPClientParser.statusReceived

    def statusReceived(self, status):
        try:
            return old_sr(self, status)
        except ParseError, e:
            if e.args[0] == 'wrong number of parts':
                return old_sr(self, status + ' OK')
            raise

    statusReceived.__doc__ == old_sr.__doc__
    HTTPClientParser.statusReceived = statusReceived


class filterConditon:
    # propogation node limit condition
    school_target = [u"复旦大学", u"华东师范大学", u"上海交通大学", u"同济大学", u"SJTU", u"sjtu", u"fdu", u"FDU", u"ECNU", u"ecnu",
                     u"上海财经大学", u"上海外国语大学", u"浙江大学", u"南京大学", u"ZJU", u"zju", u"清华大学", u"北京大学", u"THU", u"PKU"]
    followee_min = 0
    followee_max = 1000
    # target node limitation
    location_target = u"上海"
    gender_target = "female"
    follower_min = 0
    follower_max = 3000
    # ranking dict
    topic_score = {}
    stop = False


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    base = "http://www.zhihu.com"
    spider_filter = filterConditon()
    headers = {}
    sub_name = ""
    user = ""
    pwd = ""
    sub_type = ""
    pending_Q = ""
    pending_S = ""
    seen_S = ""
    success_S = ""
    cookies = dict()

    # not add header will lead to getting 500 internal error.
    def __init__(self, user=None, pwd=None, sub_name=None, start_from_redis=False,
                 start_from_file=None, sub_type=redis_const.TYPE_NO_ACCOUNT, master=False):
        if sub_type == redis_const.TYPE_HAS_ACCOUNT:
            if user is None or pwd is None or sub_name is None:
                self.logger.error("an sub_config must be given")
                exit(0)
        scrapy.Spider.__init__(self)
        self.master = master
        self.user = user
        self.pwd = pwd
        if self.master:
            self.sub_name = "master." + sub_type + "." + sub_name
        else:
            self.sub_name = "slave." + sub_type + "." + sub_name
        self.sub_type = sub_type
        self.start_from_redis = start_from_redis
        self.start_from_file = start_from_file
        self.pending_Q = redis_const.PENDING_QUEUE + self.sub_type
        self.pending_S = redis_const.PENDING_SET + self.sub_type
        self.seen_S = redis_const.SET_SEEN + self.sub_type
        self.success_S = redis_const.SET_SUCCESS + self.sub_type
        self.fail_S = redis_const.SET_FAIL + self.sub_type

        self.rclient = redis.StrictRedis(host="localhost", port=6379, db=0)

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
        self.stop = False


    def send_mail(self, subject, text, lock=600):
        self.myMail.send_timed(lock, subject + "@" + self.sub_name, text)

    def genConfig(self):
        content=self.rclient.get("crawler/web-cookie")
        dire = os.path.dirname(os.path.realpath(__file__))
        lines = map(lambda x: x.strip(" ;"), content.split(';'))
        config = open(dire + "/config.private", 'w')
        config.write("[cookies]\n")
        for line in lines:
            config.write(line + "\n")
        config.close()
        cf = ConfigParser.ConfigParser()
        f = os.path.dirname(os.path.realpath(__file__))
        cf.read(f + '/config.private')
        cookies = cf.items('cookies')
        self.cookies = dict(cookies)
        self.headers['X-Xsrftoken'] = self.cookies["_xsrf"]

    def prepare(self):
        if self.master:
            seen = self.rclient.spop(self.seen_S)
            print self.pending_S, self.pending_Q, seen
            while (seen is not None) and len(seen) < 64:
                if self.rclient.sadd(self.pending_S, seen):
                    self.rclient.rpush(self.pending_Q, seen)
                seen = self.rclient.spop(self.seen_S)
            self.genConfig()
            self.fromFile()
            self.logger.info("master prepare done!")
        else:
            self.logger.info("this is s slave,wait a sec...")
            time.sleep(5)

    def consume(self, response):
        b = "https://www.zhihu.com/people/"
        count = 50
        if self.sub_type == redis_const.TYPE_HAS_ACCOUNT:
            count = 1
        while count > 0:
            name = self.rclient.lpop(self.pending_Q)
            if name is not None:
                self.rclient.sadd(self.seen_S, name)
                self.rclient.srem(self.pending_S, name)
                yield scrapy.Request(b + name,
                                     callback=self.parse_people_info,
                                     headers=self.headers)
                if self.sub_type == redis_const.TYPE_HAS_ACCOUNT:
                    time.sleep(1)
                count -= 1
            else:
                time.sleep(20)
                break
        yield scrapy.Request("https://www.zhihu.com",
                             callback=self.backToConsume,
                             headers=self.headers)

    def backToConsume(self, response):
        yield scrapy.Request("https://www.zhihu.com",
                             callback=self.consume,
                             headers=self.headers)

    def start_requests(self):
        _monkey_patching_HTTPClientParser_statusReceived()
        self.prepare()
        if self.sub_type == redis_const.TYPE_HAS_ACCOUNT:
            yield scrapy.Request(
                "https://www.zhihu.com",
                callback=self.consume,
                headers=self.headers,
                cookies=self.cookies
            )
        elif self.sub_type == redis_const.TYPE_NO_ACCOUNT:
            yield scrapy.Request(
                "https://www.zhihu.com",
                callback=self.consume,
                headers=self.headers
            )

    def fromFile(self):
        if self.start_from_file is not None:
            f = open(self.start_from_file, 'r')
            user = f.readlines()
            user = map(lambda x: x.strip("\n"), user)
            for u in user:
                if self.rclient.sadd(self.pending_S, u):
                    self.rclient.rpush(self.pending_Q, u)

    def parse_people_list_more(self, response):
        try:
            j = json.loads(response.body)
            sel = Selector(text=" ".join(j['msg']))
            self.logger.info(response.request.headers['tracking_user_hash'])
            follower_hash = response.request.headers['tracking_user_hash']
            people = sel.xpath("//h2[@class='zm-list-content-title']//a")
            for person in people:
                # name = person.xpath("@title").extract_first(default='not-found')
                href = person.xpath("@href").extract_first(default='not-found')
                url_name = href.split('/')[-1]
                ret = items.RelationItem()
                ret["follower"] = follower_hash
                ret["followee"] = url_name
                yield ret
                self.logger.info("add to noaccount:"+href)
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
            person['bio'] = top.xpath(".//div[contains(@class,'bio')]/text()").extract_first(default='not-found')
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
            sideBar = response.selector.xpath(
                ".//div[@class='zu-main-sidebar']/div[@class='zm-profile-side-following zg-clear']")
            person['followee_num'] = sideBar.xpath("a[1]/strong/text()").extract_first(default='not-found')
            person['follower_num'] = sideBar.xpath("a[2]/strong/text()").extract_first(default='not-found')

            yield person

            if self.sub_type == redis_const.TYPE_NO_ACCOUNT:
                if self.judge_person_as_target(person) and (not self.judge_person_as_valid_source(person)):
                    target = items.TargetPersonItem()
                    target['hash_id'] = person['hash_id']
                    yield target
                elif self.judge_person_as_valid_source(person):
                    tosend = items.SendToAccountItem()
                    tosend["url_name"] = person['url_name']
                    yield tosend
            else:
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
                        time.sleep(0.5)
        except Exception, e:
            self.send_mail("parse_people_info", str(
                e) + "response:" + response.url + "\nresponse_body:" + response.body + "request:" + response.request.url)
'''
    def parse_people_info_mob(self, response):
        try:
            j = json.loads(response.body)
            if "error" in j:
                self.send_mail("parse_people_error", response.body)
            person = items.PersonItem()
            person["image_href"] = j["avatar_url"].replace("_s.", "_l.")
            person["url_name"] = ""
            person["hash_id"] = j['id']
            person["name"] = j['name']
            person["bio"] = j['headline']
            try:
                person['city'] = j['locations'][0]['name']
            except:
                person['city'] = 'not-found'
            person["if_female"] = (j['gender'] == 0)
            try:
                person['school'] = j['educations'][0]['school']['name']
            except:
                person['school'] = 'not-found'
            try:
                person['major'] = j['educations'][0]['major']['name']
            except:
                person['major'] = 'not-found'
            person['introduction'] = j['description']
            person['agree_num'] = j['voteup_count']
            person['follower_num'] = j['follower_count']
            person['followee_num'] = j['following_count']
            '''