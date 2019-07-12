# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from xiudong.dbhelper.mysqlhelper import MysqlHelper
import json


# 保存音乐人信息
class artistPipeline(object):

    def __init__(self):
        self.helper = MysqlHelper()

    def process_item(self, item, spider):
        params = (item['detail_url'], item['name'], item['artist_img'], item['area'], item['style'], item['introduce'],
                  json.dumps(item['about_img_list'], ensure_ascii=False),
                  json.dumps(item['music_works_list'], ensure_ascii=False))
        sql_str = "INSERT INTO t_artist(detail_url, `name`, artist_img, area,style,introduce,about_imgs,music_works) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % params
        self.helper.insert(sql_str)
        print("写入数据：" + str(item['name']))
        return item

    def close_spider(self, spider):
        self.helper.close()

# 保存演出信息
class showPipeline(object):

    def __init__(self):
        self.helper = MysqlHelper()

    def process_item(self, item, spider):
        params = (item['detail_url'], item['show_name'], item['show_img'], item['show_time'],
                  item['show_place'],item['show_addr'],item['show_phone'],item['show_sponsor'],
                  json.dumps(item['show_tag_list'], ensure_ascii=False),
                  json.dumps(item['show_price_list'], ensure_ascii=False),
                  json.dumps(item['show_artists'], ensure_ascii=False),
                  json.dumps(item['show_details'], ensure_ascii=False),
                  json.dumps(item['show_music_dict'], ensure_ascii=False),
                  json.dumps(item['show_about_imgs_list'], ensure_ascii=False))
        sql_str = "INSERT INTO t_show(detail_url, show_name, show_img, show_time,show_place,show_addr,show_phone," \
                  "show_sponsor,show_tag_list,show_price_list,show_artists,show_details,show_music_dict,show_about_imgs_list) " \
                  "VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % params
        self.helper.insert(sql_str)
        print("写入数据：" + str(item['name'])+str(item['detail_url']))
        return item

    def close_spider(self, spider):
        self.helper.close()
