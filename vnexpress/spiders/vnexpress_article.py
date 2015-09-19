#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor  as lxml
import scrapy
import pdb
import html2text
from elasticsearch import Elasticsearch
import re
from  scrapy.exceptions import CloseSpider


class Article(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()


es_client = Elasticsearch()
index_name = "vietnam"
doctype = "article"

# es_client.index(index=index_name, doc_type=doctype, id=self.text, body=self.to_dict())

def write_to_file(filename, result):
    output = open(filename, 'wb')
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

    def add_text(self, text):
        data = re.sub("”|\"|\n|`|-|=|[|]|'|;|/|\.|,|~|!|@|#|$|%|^|&|\*|:|\(|\)|_|\+|}|{|>|<|\?", " ", text)
        for sub in data.split(" "):
            #text_clean= sub.replace("â€","")
            text_clean = sub.strip().lower()
            if len(text_clean) >1 and text_clean.isdigit() == False and text_clean not in self.words:
                self.words.append(text_clean)


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
            if self.is_write == False and len(self.words) > 200000:
                print "Write to file "
                self.is_write = True
                unique_terms= set(self.words)
                print "lengh1 %s length2 %s"%(len(self.words),len(unique_terms))
                write_to_file("vietnam.txt", unique_terms)
                raise CloseSpider('bandwidth_exceeded')
            else:
                print "lengh1 %s " %(len(self.words))
                self.add_big_text(results)
        except:
            return None


def closed(self, reason):
    print "close"

        



