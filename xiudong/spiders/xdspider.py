# -*- coding: utf-8 -*- 
# @File : xdspider.py

import scrapy
from xiudong.items import artistItem


class xdSpider(scrapy.Spider):
    name = "xiudong"
    allowed_domains = ["www.showstart.com"]
    offset = 1
    url = "https://www.showstart.com/artist/list?pageNo="
    start_urls = [url + str(offset)]
    artist_page_list_temp = []

    def parse(self, response):
        self.get_artist_lists(response)
        # 遍历所有详情页url
        # for artist_item in self.artist_page_list_temp:
        #     yield scrapy.Request(str(artist_item), callback=self.artist_parse)
        # 单条数据测试
        yield scrapy.Request(str(self.artist_page_list_temp[1]), callback=self.artist_parse)
        # self.get_next_page()

    # 解析音乐人详情页数据
    def artist_parse(self, response):
        # print(response.text)
        artistItem.detail_url = response.url
        name_xpath = response.xpath('//div[@class="main"]//div[@class="name"]/text()')
        artist_img_xpath = response.xpath('//div[@class="main"]//div[@class="profile-photo ll"]//img/@original')
        area_style_xpath = response.xpath('//div[@class="main"]//ol[@class="dec"]/li/text()')
        introduce_xpath = response.xpath('//div[@class="main"]//div[@class="detalils-wrap"]//div[@id="tab1"]//p')
        about_img_xpath = response.xpath('//div[@class="main"]//div[@class="detalils-wrap"]//div[@id="tab7"]//li/a/@href')
        music_works_xpath = response.xpath('//*[@id="tab4"]/div/ul/li')
        print(music_works_xpath.extract())
        # 音乐人名称
        if len(name_xpath) > 0:
            artistItem.name = str(name_xpath[0].extract()).replace(" ","")
        # 图片
        if len(artist_img_xpath) > 0:
            artistItem.artist_img = artist_img_xpath[0].extract()
        # 地区
        if len(area_style_xpath) > 0:
            artistItem.area = str(area_style_xpath[0].extract()).replace(" ","").replace("\t","").replace("\r","").replace("\n","").replace("地区：","")
        # 风格
        if len(area_style_xpath) > 1:
            artistItem.style = str(area_style_xpath[1].extract()).replace(" ","").replace("\t","").replace("\r","").replace("\n","").replace("风格：","")
        else:
            artistItem.style = ""
        # 简介
        if len(introduce_xpath) > 0:
            # print(type(introduce_xpath.extract()))
            artistItem.introduce = str(introduce_xpath.xpath('string(.)')[0].extract()).replace(" ","").replace("\t","").replace("\r","").replace("\n","").replace('<br>','')
        else:
            artistItem.introduce = "暂无简介"
        # 相关图片
        artistItem.about_img_list = []
        for about_img_item in about_img_xpath:
            artistItem.about_img_list.append(about_img_item.extract())
        # 作品集
        artistItem.music_works_list = []
        for music_item in music_works_xpath:
            music_dict = {}
            music_name = str(music_item.xpath('./span[@class="a-link"]/text()')[0].extract()).replace(" ","").replace("\t","").replace("\r","").replace("\n","")
            music_play_url = str(music_item.xpath('div[@class="jp-jplayer"]/@playsrc').extract_first()).replace(" ","").replace("\t","").replace("\r","").replace("\n","")
            music_dict["music_name"] = music_name
            music_dict["music_play_url"] = music_play_url
            music_dict["music_player"] = artistItem.name
            artistItem.music_works_list.append(music_dict)
        print(artistItem.name)
        print(artistItem.artist_img)
        print(artistItem.area)
        print(artistItem.style)
        print(artistItem.introduce)
        print(artistItem.about_img_list)
        print(artistItem.music_works_list)
        yield artistItem

    # 解析音乐人列表，获取音乐人详情页url
    def get_artist_lists(self, response):
        self.artist_page_list_temp.clear()
        links = response.xpath('//div[@class="main auto-width"]//ul//li')
        for linkItem in links:
            link_href_item = linkItem.xpath('.//a[@class="g-name a-link"]/@href').extract()
            if len(link_href_item) > 0:
                self.artist_page_list_temp.append(link_href_item[0])

    # 获取下一页音乐人列表
    def get_next_page(self):
        self.offset += 1
        if self.offset <= 1198:
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

