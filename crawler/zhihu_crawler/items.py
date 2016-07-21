# -*- coding: utf-8 -*-
import scrapy


class RelationItem(scrapy.Item):
    """
     field are user hash name(name in url)
    """
    follower = scrapy.Field()
    followee = scrapy.Field()


class PersonItem(scrapy.Item):
    name = scrapy.Field()
    hash = scrapy.Field()
    school = scrapy.Field()
    city = scrapy.Field()
    major = scrapy.Field()
    gender = scrapy.Field()
    image_href = scrapy.Field()
    follower_num = scrapy.Field()
    followee_num = scrapy.Field()
    bio = scrapy.Field()
    introduction = scrapy.Field()
    agree_num = scrapy.Field()


class TopicFollowItem(scrapy.Item):
    hash = scrapy.Field()
    topic_followed = scrapy.Field()
