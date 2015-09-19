#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor  as lxml
import html2text
import redis
from  scrapy.exceptions import CloseSpider


class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', **redis_kwargs):
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)


def clean_string(value):
    return ' '.join(value.split()).strip().replace('\x00', '')


def write_word_list(filename, result):
    output = open(filename, 'a')
    output.writelines(["%s\n" % item.encode('utf-8') for item in result])
    output.close()


class VnexpressArticle(CrawlSpider):
    name = "vnexpress"
    start_urls = ["http://vnexpress.net"]
    # start_urls = ["http://vnexpress.net/tin-tuc/thoi-su"]
    cpt = 0
    words = [];
    rules = [
        Rule(lxml(allow=(".*vnexpress.net.*"), restrict_xpaths=("//div[@class='pagination_news right']//a")),
             follow=True),
        Rule(lxml(allow=(".*vnexpress.net.*"), restrict_xpaths=("//ul[@id='menu_web']/li/a")), follow=True),
        Rule(lxml(allow=(".*vnexpress.net.*"), restrict_xpaths=("//ul[@id='breakumb_web']/li/a")), follow=True),
        Rule(lxml(allow=(".*vnexpress.net.*"), restrict_xpaths=("//ul[@id='news_home']/li/div/div/a[1]")),
             callback='create_article'),
    ]
    is_write = False
    queue = RedisQueue("vietnam", host="107.155.114.223")
    word_to_write_list = []

    def write_to_file(self, word):
        self.word_to_write_list.append(word)
        if len(self.word_to_write_list) % 1000 == 0:
            write_word_list("vietnam.txt", self.word_to_write_list)
            self.word_to_write_list = []


    def add_text(self, text):
        data = re.sub("”|\"|\n|`|-|=|[|]|'|;|/|\.|,|~|!|@|#|$|%|^|&|\*|:|\(|\)|_|\+|}|{|>|<|\?", " ", text)
        for sub in data.split(" "):
            # text_clean= sub.replace("â€","")
            text_clean = sub.strip().lower()
            if len(text_clean) > 1 and text_clean.isdigit() == False and text_clean not in self.words:
                self.words.append(text_clean)
                self.queue.put({"lang": "vietnam", "keyword": text_clean})
                self.write_to_file(text_clean)


    def add_big_text(self, results):
        for result in results:
            data = html2text.html2text(result.extract())
            self.add_text(data)

    def create_article(self, response):
        try:
            title = response.xpath(
                "//div[@id='detail_page']//div[contains(@class,'main_content_detail')]//div[@class='title_news']/h1/text()")[
                0].extract()
            results = response.xpath(
                "//div[@id='detail_page']//div[contains(@class,'main_content_detail')]//div[@id='left_calculator']//div[@class='fck_detail width_common']//p//text()")
            self.add_big_text(results)
            print "Length %s " % (len(self.words))
        except:
            return None


def closed(self, reason):
    print "close"

        



