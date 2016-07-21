# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json

'''
 field are user hash name(name in url)
'''


class RelationItem(scrapy.Item):
    follower = scrapy.Field()
    followee = scrapy.Field()


class PersonItem(scrapy.Item):
    name = scrapy.Field()
    hash = scrapy.Field()
    school = scrapy.Field()
    major = scrapy.Field()
    gender = scrapy.Field()
    image_href = scrapy.Field()
    follower_num = scrapy.Field()
    followee_num = scrapy.Field()
    bio = scrapy.Field()
    introduction = scrapy.Field()
    topic_followed = scrapy.Field()
    ask_num = scrapy.Field()
    answer_num = scrapy.Field()
    agree_num = scrapy.Field()
