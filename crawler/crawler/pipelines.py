# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import items
import json
import redis_const


class RedisPipeline(object):
    def __init__(self):
        self.rclient = redis.StrictRedis(host="localhost", port=6379, db=0)

    def process_item(self, item, spider):
        if isinstance(item, items.RelationItem):
            self.process_relation_item(item, spider)
        elif isinstance(item, items.PersonItem):
            self.process_person_item(item, spider)
        elif isinstance(item, items.TopicFollowItem):
            self.process_topicfollow_item(item, spider)
        elif isinstance(item, items.TargetPersonItem):
            self.process_targetperson_item(item, spider)
        elif isinstance(item, items.PropogationPersonItem):
            self.process_propogationperson_item(item, spider)
        elif isinstance(item, items.SendToAccountItem):
            self.process_sendtoaccount_item(item, spider)
        return item

    def process_relation_item(self, item, spider):
        if item['follower'] != 'not-found' and item['followee'] != 'not-found':
            self.rclient.sadd("followees/" + item['follower'], item['followee'])
            self.sendToNoAccount(item['followee'])
        else:
            spider.send_mail("process_relation_item_exception", str(item))

    def process_person_item(self, item, spider):
        d = dict(item)
        if item["name"] == "not-found" and len(item["hash_id"]) != 32:
            spider.send_mail("format error person", json.dumps(d))
            return
        self.rclient.sadd(spider.success_S, item["url_name"])
        self.rclient.srem(spider.seen_S, item["url_name"])

        if item["if_female"]:
            self.rclient.set("people/" + item["hash_id"], json.dumps(d))
            self.rclient.set("hash/" + item["url_name"], item["hash_id"])

    def process_targetperson_item(self, item, spider):
        self.rclient.sadd("target_people", item["hash_id"])

    def process_propogationperson_item(self, item, spider):
        self.rclient.sadd("propogation_people", item["hash_id"])

    def process_topicfollow_item(self, item, spider):
        pass

    def sendToAccount(self, name):
        if (not self.rclient.sismember(redis_const.SET_SEEN_HAS_ACCOUNT, name)) and (
                not self.rclient.sismember(redis_const.SET_SUCCESS_HAS_ACCOUNT, name)):
            if self.rclient.sadd(redis_const.PENDING_SET_HAS_ACCOUNT, name) == 1:
                self.rclient.rpush(redis_const.PENDING_QUEUE_HAS_ACCOUNT, name)

    def sendToNoAccount(self, name):
        if (not self.rclient.sismember(redis_const.SET_SEEN_NO_ACCOUNT, name)) and (
                not self.rclient.sismember(redis_const.SET_SUCCESS_NO_ACCOUNT, name)):
            if self.rclient.sadd(redis_const.PENDING_SET_NO_ACCOUNT, name) == 1:
                self.rclient.rpush(redis_const.PENDING_QUEUE_NO_ACCOUNT, name)

    def process_sendtoaccount_item(self, item, spider):
        self.sendToAccount(item['url_name'])
