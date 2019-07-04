# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class artistItem(scrapy.Item):
    # 秀动url
    detail_url = scrapy.Field()
    # 名称
    name = scrapy.Field()
    # 乐队图片
    artist_img = scrapy.Field()
    # 地区
    area = scrapy.Field()
    # 风格
    style = scrapy.Field()
    # 简介
    introduce = scrapy.Field()
    # 相关图片
    about_img_list = scrapy.Field()
    # 音乐作品
    music_works_list = scrapy.Field()
