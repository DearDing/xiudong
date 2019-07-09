# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 音乐人
class artistItem(scrapy.Item):
    # 音乐人详情页url
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

# 演出
class showItem(scrapy.Item):
    # 演出详情页url
    detail_url = scrapy.Field()
    # 演出名称
    show_name = scrapy.Field()
    # 图片
    show_img = scrapy.Field()
    # 演出时间
    show_time = scrapy.Field()
    # 艺人
    show_artists = scrapy.Field()
    # 场地
    show_place = scrapy.Field()
    # 地址
    show_addr = scrapy.Field()
    # 电话
    show_phone = scrapy.Field()
    # 标签
    show_tag_list = scrapy.Field()
    # 价格列表
    show_price_list = scrapy.Field()
    # 演出详情
    show_details = scrapy.Field()
    # 演出主办方--
    show_sponsor = scrapy.Field()
    # 相关图片--
    show_about_imgs_list = scrapy.Field()
    # 音乐作品--
    show_music_dict = scrapy.Field()


