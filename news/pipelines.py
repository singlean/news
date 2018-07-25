# -*- coding: utf-8 -*-

from pymongo import MongoClient

class XLZTPipeline(object):

    def open_spider(self, spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["xlzt"]

    def process_item(self, item, spider):
        if spider.name == "xlzt":
            self.collection.insert(item)
            print("保存成功")
            # pprint.pprint(item)
        return item


class SGWXPipeline(object):

    def open_spider(self, spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["sgwx"]

    def process_item(self, item, spider):
        if spider.name == "sgwx":
            self.collection.insert(item)
            print("保存成功")
            # pprint.pprint(item)
        return item



























