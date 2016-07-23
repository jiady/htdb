# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import items


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
        return item

    def process_relation_item(self, item, spider):
        self.rclient.sadd("followees/" + item['follower'], item['followee'])

    def process_person_item(self, item, spider):
        self.rclient.set("people/" + item["hash_id"], str(item))
        self.rclient.set("hash/" + item["url_name"], item["hash_id"])

    def process_targetperson_item(self, item, spider):
        self.rclient.sadd("target_people", item["hash_id"])

    def process_propogationperson_item(self, item, spider):
        self.rclient.sadd("propogation_people", item["hash_id"])

    def process_topicfollow_item(self, item, spider):
        pass
