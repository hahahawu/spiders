# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from blogchinaSpider.settings import IPPOOL


class MyproxiesSpiderMiddleware(object):
    def __init__(self, ip=''):
        self.ip = ip

    @staticmethod
    def process_request(request, spider):
        thisIp = random.choice(IPPOOL)
        print("this is ip:" + thisIp["ipaddr"])
        request.meta["proxy"] = "http://" + thisIp["ipaddr"]