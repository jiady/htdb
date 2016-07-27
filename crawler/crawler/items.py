# -*- coding: utf-8 -*-
import scrapy


class RelationItem(scrapy.Item):
    """
     follower is user-hash
     followee is uesr-url-name
    """
    follower = scrapy.Field()
    followee = scrapy.Field()


class PersonItem(scrapy.Item):
    name = scrapy.Field()
    url_name = scrapy.Field()
    hash_id = scrapy.Field()
    school = scrapy.Field()
    city = scrapy.Field()
    major = scrapy.Field()
    if_female = scrapy.Field()
    image_href = scrapy.Field()
    follower_num = scrapy.Field()
    followee_num = scrapy.Field()
    bio = scrapy.Field()
    introduction = scrapy.Field()
    agree_num = scrapy.Field()


class TargetPersonItem(scrapy.Item):
    hash_id = scrapy.Field()

class PropogationPersonItem(scrapy.Item):
    hash_id = scrapy.Field()

class TopicFollowItem(scrapy.Item):
    hash_id = scrapy.Field()
    topic_followed = scrapy.Field()

class SendToAccountItem(scrapy.Item):
    url_name = scrapy.Field()
