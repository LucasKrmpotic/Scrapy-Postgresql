 import datetime

from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from codeworkers.items import CodeworkersItem

class CompuTrabajoSpider(CrawlSpider):
    name = "computrabajo"
    item_count = 0
    allowed_domains = ["www.computrabajo.com.ar"]
    start_urls = (
        'https://www.computrabajo.com.ar/trabajo-de-programador',
    )
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//li[@class="siguiente"]/a')),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="js-o-link"]'),
             callback='parse_item')
    )

    def parse_item(self, response):
        l = ItemLoader(item=CodeworkersItem(), response=response)

        l.add_xpath('titulo', '//*[@id="MainContainer"]//h1')
        
        l.add_value('url', response.url)
        self.item_count += 1
        if self.item_count > 5:
            raise CloseSpider('item_exceeded')
        return l.load_item()

    
class BumeranSpider(CrawlSpider):
    name = "bumeran"
    item_count = 0
    allowed_domains = ["www.bumeran.com.ar"]
    start_urls = (
        'http://www.bumeran.com.ar/empleos-busqueda-programador.html',
    )
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="pagination col-md-12"]/li[8]/a')),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="col-sm-9 col-md-10 wrapper"]/a'),
             callback='parse_item')
    )

    def parse_item(self, response):
        l = ItemLoader(item=CodeworkersItem(), response=response)

        l.add_xpath('titulo', '//h1[@class="aviso_title"]')
        l.add_value('url', response.url)
        self.item_count += 1
        if self.item_count > 5:
            raise CloseSpider('item_exceeded')
        return l.load_item()


class ZonaJobsSpider(CrawlSpider):
    name = "zonajobs"
    item_count = 0
    allowed_domains = ["www.zonajobs.com.ar"]
    start_urls = (
        'https://www.zonajobs.com.ar/ofertas-de-trabajo-programador.html',
    )
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="pagination col-md-12"]/li[8]/a')),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="col-sm-9 col-md-10 wrapper"]/a'),
             callback='parse_item')
    )

    def parse_item(self, response):
        l = ItemLoader(item=CodeworkersItem(), response=response)

        l.add_xpath('titulo', '//h1[@class="aviso_title"]')
        l.add_value('url', response.url)
        self.item_count += 1
        if self.item_count > 5:
            raise CloseSpider('item_exceeded')
        return l.load_item()

class LaWebDelProgramadorSpider(CrawlSpider):
    name = "lawebdelprogramador"
    item_count = 0
    allowed_domains = ["www.lawebdelprogramador.com"]
    start_urls = (
        'https://www.lawebdelprogramador.com/trabajo/32-Argentina/index1.html',
    )
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pageb"]/a[6]')),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="ce listRow2 listRowJob newBlock"]/div/h2/a'),
             callback='parse_item')
    )

    def parse_item(self, response):
        l = ItemLoader(item=CodeworkersItem(), response=response)

        l.add_xpath('titulo', '//h1')
        l.add_value('url', response.url)
        self.item_count += 1
        if self.item_count > 5:
            raise CloseSpider('item_exceeded')
        return l.load_item()

class StackOverflowSpider(CrawlSpider):
    name = "stackoverflow"
    item_count = 0
    allowed_domains = ["stackoverflow.com"]
    start_urls = (
        'https://stackoverflow.com/jobs?med=site-ui&ref=jobs-tab',
    )
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@class="prev-next job-link test-pagination-next"]')),
        Rule(LinkExtractor(restrict_xpaths='//h2[@class="g-col10"]/a'),
             callback='parse_item')
    )

    def parse_item(self, response):
        l = ItemLoader(item=CodeworkersItem(), response=response)

        l.add_xpath('titulo', '//h1[@class="-title"]/a/text()')
        l.add_value('url', response.url)
        self.item_count += 1
        if self.item_count > 5:
            raise CloseSpider('item_exceeded')
        return l.load_item()
