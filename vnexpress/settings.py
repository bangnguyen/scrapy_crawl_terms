# -*- coding: utf-8 -*-

# Scrapy settings for vnexpress project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#





BOT_NAME = 'vnexpress'

SPIDER_MODULES = ['vnexpress.spiders']
NEWSPIDER_MODULE = 'vnexpress.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'vnexpress (+http://www.yourdomain.com)'

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
