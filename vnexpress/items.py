# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class VnexpressItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
#response.xpath("//div[ @id='detail_page']//div[contains(@class,'main_content_detail')]//div[@class='title_news']/h1/text()")[0].extract()