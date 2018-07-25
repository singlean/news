# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_redis.spiders import RedisSpider
from pprint import pprint
from copy import deepcopy

class SgwxSpider(RedisSpider):
    name = 'sgwx'
    allowed_domains = ['sogou.com',"qq.com"]
    # start_urls = ['http://weixin.sogou.com/weixin?query=python']
    redis_key = "sgwx"

    def parse(self, response):

        # 公众号列表
        li_list = response.xpath("//ul[@class='news-list2']/li")
        for li in li_list:
            item = {}
            title = li.xpath(".//div[@class='txt-box']/p[@class='tit']/a//text()").extract()
            item["public_title"] = ""
            for i in title:
                item["public_title"] += i.strip()

            item["public_href"] = li.xpath(".//div[@class='txt-box']/p[@class='tit']/a/@href").extract_first()
            # 微信号
            item["public_wid"] = li.xpath(".//label[@name='em_weixinhao']/text()").extract_first()

            desc = li.xpath("./dl[1]/dd//text()").extract()
            item["desc"] = ""
            for i in desc:
                item["desc"] += i.strip()

            new_ess = li.xpath("./dl[2]/dd//text()").extract()
            if new_ess:
                item["new_ess"] = ""
                for i in new_ess:
                    item["new_ess"] += i.strip()
                item["new_ess"] = re.sub(r"document.write\(timeConvert\('\d+?'\)\)","",item["new_ess"])

            item["public_img"] = li.xpath(".//div[@class='img-box']//img/@src").extract_first()
            if item["public_img"]:
                item["public_img"] = "http:" + item["public_img"]

            yield scrapy.Request(
                url=item["public_href"],
                callback=self.parse_pub_detail,
                meta={"item":item}
            )

        # 下一页
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url:
            next_url = "http://weixin.sogou.com/weixin" + next_url

            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )



    def parse_pub_detail(self,response):
        item = response.meta["item"]

        html = re.findall(r' var msgList = {"list":(.*?)seajs\.use',response.body.decode(),re.S)[0] if len(re.findall(r' var msgList = {"list":(.*?)seajs\.use',response.body.decode(),re.S)) else None

        if html:
            ess_list = re.findall(r'"content_url":"(.*?)".*?"subtype":\d+?,"title":"(.*?)"',html,re.S)
            for ess in ess_list:
                item["essay_url"] = "https://mp.weixin.qq.com" + re.sub(r"amp;","",ess[0])
                item["essay_title"] = ess[1]

                yield scrapy.Request(
                    url=item["essay_url"],
                    callback=self.parse_ess_detail,
                    meta={"item":deepcopy(item)}
                )

    def parse_ess_detail(self,response):
        item = response.meta["item"]

        p_list = response.xpath("//div[@id='js_content']/p//text()").extract()
        item["ess_content"] = ""
        for p in p_list:
            if p.strip():
                item["ess_content"] += p.strip()
        item["ess_img"] = response.xpath("//div[@id='js_content']/p/img/@src").extract()

        # print(item)
        yield item















































