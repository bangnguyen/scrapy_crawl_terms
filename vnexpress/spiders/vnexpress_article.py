from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as lxml
import scrapy
import pdb
import html2text
from elasticsearch import Elasticsearch
class Article(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()


es_client = Elasticsearch()
index_name = "vietnam"
doctype = "article"

#es_client.index(index=index_name, doc_type=doctype, id=self.text, body=self.to_dict())


class VnexpressArticle(CrawlSpider):
    name = "vnexpress"
    start_urls = ["http://vnexpress.net"]
    #start_urls = ["http://vnexpress.net/tin-tuc/thoi-su"]
    cpt = 0
    rules = [
        Rule(lxml(allow=(".*vnexpress.net.*"),restrict_xpaths=("//div[@class='pagination_news right']//a")),follow=True),
        Rule(lxml(allow=(".*vnexpress.net.*"),restrict_xpaths=("//ul[@id='menu_web']/li/a")),follow=True),
        Rule(lxml(allow=(".*vnexpress.net.*"),restrict_xpaths=("//ul[@id='breakumb_web']/li/a")),follow=True),
        Rule(lxml(allow=(".*vnexpress.net.*"),restrict_xpaths=("//ul[@id='news_home']/li/div/div/a[1]")),callback='create_article'),
    ]


    def create_article(self, response):
        try:
            title = response.xpath("//div[@id='detail_page']//div[contains(@class,'main_content_detail')]//div[@class='title_news']/h1/text()")[0].extract()
            data = response.xpath("//div[@id='detail_page']//div[contains(@class,'main_content_detail')]//div[@id='left_calculator']//div[@class='fck_detail width_common']")
            description = html2text.html2text(data.extract()[0])
            item = Article()
            item ['title'] = title
            item['url'] = response.url
            item['description'] = description
            self.cpt +=1
            if self.cpt <=20000:
                print self.cpt
                print item['url']
                es_client.index(index=index_name, doc_type=doctype, id=item['url'], body={"title":item["title"],"description":item["description"]})
                return item
        except:
            return None




    def closed(self, reason):
        print "close"

        



