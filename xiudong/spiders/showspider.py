# -*- coding: utf-8 -*- 
# @File : showspider.py

import scrapy
from xiudong.items import showItem


class showSpider(scrapy.Spider):
    name = "show_spider"
    allowed_domains = ["www.showstart.com"]

    offset = 1
    url = "https://www.showstart.com/event/list?isList=1&pageNo="
    start_urls = [url + str(offset)]

    show_page_list_temp = []

    def parse(self, response):
        # print(response.text)
        self.get_details_url(response)
        # 遍历所有详情页url
        # for show_item in self.show_page_list_temp:
        #     yield scrapy.Request(str(show_item), callback=self.show_parse)
        # 单条数据测试
        # yield scrapy.Request(str(self.show_page_list_temp[1]), callback=self.show_parse)
        yield scrapy.Request("https://www.showstart.com/event/87018", callback=self.show_parse)
        # 获取列表下一页
        # self.get_next_page()

    # 解析演出详情页数据
    def show_parse(self, response):
        # print(response.text)
        showItem.detail_url = response.url
        img_sellist = response.xpath('//div[@class="goods-wrap"]//a/img/@original')
        name_sellist = response.xpath('//div[@class="goods-wrap"]//div[@class="items ll"]/h1[@class="goods-name"]/text()')
        list_sellist = response.xpath('//div[@class="goods-wrap"]//div[@class="items ll"]//ul[@class="items-list"]/li')
        tag_sellist = response.xpath('//div[@class="goods-wrap"]//div[@class="items ll"]//div[@class="goods-type"]/span/text()')
        price_sellist = response.xpath('//div[@class="goods-wrap"]//div[@class="stamp ll"]//ul[@class="ticket MT30"]/li')
        show_details_sellist = response.xpath('//div[@class="n-tab-content"]//div[@class="group"]//div[@class="dec"]/text()')
        sponsor_sellist = response.xpath('//div[@class="detalils-wrap"]//div[@class="n-tab-content"]//div[@class="list-item activity-hoster ll"]//div[@class="info"]/p/text()')
        imgs_sellist = response.xpath('//div[@class="n-tab-content"]//div[@class="group"]//ul[@class="img-list justify"]/li//img/@original')
        music_sellist = response.xpath('//div[@class="n-tab-content"]//div[@class="group"]//ul[@class="music-list MT20"]/li')
        # 图片
        if len(img_sellist) > 0:
            showItem.show_img = img_sellist.extract_first()
        # 演出名称
        if len(name_sellist) > 0:
            showItem.show_name = name_sellist.extract()[-1].strip()
        # 演出时间
        showItem.show_time = list_sellist[0].xpath('./text()').extract_first().replace(" ","").replace("\t","").replace("\r","").replace("\n","")
        # 艺人
        showItem.show_artists = []
        artists_sellist = list_sellist[1].xpath('./a/text()')
        for artist_item in artists_sellist:
            showItem.show_artists.append(artist_item.extract())
        # 场地
        showItem.show_place = list_sellist[2].xpath('./a/text()').extract_first()
        # 地址
        showItem.show_addr = list_sellist[3].xpath('./text()').extract_first().replace(" ","").replace("\t","").replace("\r","").replace("\n","")
        # 电话
        showItem.show_phone = list_sellist[4].xpath('./text()').extract_first().replace("电话：","").replace(" ","").replace("\t","").replace("\r","").replace("\n","")
        # 标签
        showItem.show_tag_list = []
        for tag_item in tag_sellist:
            showItem.show_tag_list.append(tag_item.extract())
        # 价格 -- status -- 1：没有库存，2：未开始售票，3：售票结束，4：售票中，5：活动取消，6：审核中
        showItem.show_price_list = []
        for price_item in price_sellist:
            price_item_dict = {}
            price_item_dict["status"] = price_item.xpath('./@status').extract_first()
            price_item_dict["starttime"] = price_item.xpath('./@starttime').extract_first()
            price_item_dict["endtime"] = price_item.xpath('./@endtime').extract_first()
            price_item_dict["costprice"] = price_item.xpath('./@costprice').extract_first()
            price_item_dict["sellingprice"] = price_item.xpath('./@sellingprice').extract_first()
            price_item_dict["ticketname"] = price_item.xpath('./@ticketname').extract_first()
            showItem.show_price_list.append(price_item_dict)
        # 演出详情
        showItem.show_details = show_details_sellist.extract_first()
        # 主办方
        if len(sponsor_sellist) > 0:
            showItem.show_sponsor = sponsor_sellist.extract_first()
        else:
            showItem.show_sponsor = ""
        # 相关图片
        showItem.show_about_imgs_list = []
        for img_item in imgs_sellist:
            showItem.show_about_imgs_list.append(img_item.extract())
        # 音乐作品
        showItem.show_music_dict = {}
        for music_item in music_sellist:
            showItem.show_music_dict["music_name"] = music_item.xpath('./span[@class="a-link"]/text()').extract_first()
            showItem.show_music_dict["music_artist"] = music_item.xpath('./span[@class="singing"]/a/text()').extract_first()
            showItem.show_music_dict["music_url"] = music_item.xpath('./div[@class="jp-jplayer"]/@playsrc').extract_first()
        yield showItem

    # 获取演出详情页url
    def get_details_url(self, response):
        print(response.text)
        self.show_page_list_temp.clear()
        show_selector_list = response.xpath('//div[@class="main auto-width"]//ul[@class="g-list-wrap justify MT30"]//li/a/@href')
        # name_selector_list = response.xpath('//div[@class="main auto-width"]//ul[@class="g-list-wrap justify MT30"]//li/a/@title').extract()
        # for item in name_selector_list:
        #     print(item)
        for selector_item in show_selector_list:
            # print(selector_item.extract())
            self.show_page_list_temp.append(selector_item.extract())

    # 获取下一页演出列表
    def get_next_page(self):
        self.offset += 1
        if self.offset <= 267:
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
