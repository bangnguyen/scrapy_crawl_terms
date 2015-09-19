"""
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as lxml
import os
import pdb
from selenium import webdriver



import time
from selenium import webdriver
import pdb
from PIL import Image

chrome_path = "lib/chromedriver"
#driver = webdriver.Chrome(chrome_path)


def random_file_name():
    return str(int(time.time()))+".png"


def refresh_and_save(url):
#    driver.get(url)
    file_name = random_file_name()
#    driver.save_screenshot(file_name)
    img = Image.open(file_name)
    banner_name = random_file_name()
    #banner 1
    img.crop((275,41,1000,130)).save(banner_name)
    #banner 2
    img.crop((700,230,1000,615)).save(random_file_name())



class ProsourceSpider(CrawlSpider):
    name = "vn"
    start_urls = ["http://vnexpress.net/"]
    rules = [
        Rule(lxml(allow=("http://vnexpress.net/"),restrict_xpaths=("//ul[@id='menu_web']/li/a")),callback='add_url'),
    ]


    def add_url(self, response):
        print response.url
        #refresh_and_save(response.url)


    def closed(self, reason):
        print "close"



"""