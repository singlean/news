# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy


class XlztSpider(RedisSpider):
    name = 'xlzt'
    allowed_domains = ['com.cn']
    # start_urls = ['http://news.sina.com.cn/zt/']
    redis_key = "xlzt"

    def parse(self, response):

        # 新浪新闻专题列表
        a_list = response.xpath("//p[@class='topNav2 clearfix']/a")
        zt_list = a_list[1:17]
        zt_list.append(a_list[-1:])
        zt_list.append(a_list[-3:-2])

        for zt in zt_list:
            item = {}
            item["zt_href"] = zt.xpath("./@href").extract_first()
            item["zt_title"] = zt.xpath("./text()").extract_first()

            yield scrapy.Request(
                url=item["zt_href"],
                callback=self.parse_zt_list,
                meta={"item":item}
            )

    def parse_zt_list(self,response):

        item = response.meta["item"]
        # 新闻标题列表
        li_list = response.xpath("//ul[@class='ul_list1']/li")
        for li in li_list:
            item["news_href"] = li.xpath("./a/@href").extract_first()
            item["news_title"] = li.xpath("./a/text()").extract_first()
            l_time = li.xpath("./text()").extract_first()
            if l_time:
                if l_time.split():
                    item["l_time"] = l_time
            s_time = li.xpath("./span[@class='pg01']/text()").extract()
            if s_time:
                item["s_time"] = [i.split() for i in s_time if i.split()]

            yield deepcopy(item)











































