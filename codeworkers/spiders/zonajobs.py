import datetime

from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from codeworkers.items import CodeworkersItem

class ZonaJobsSpider(CrawlSpider):
    """ Araña para extraer ofertas de trabajo del sitio zonajobs """
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
        """ Parsea propiedades de una página.

        @url https://www.zonajobs.com.ar/ofertas-de-trabajo-programador.html
        @returns items 1
        @scrapes titulo ubicacion empresa tiempo_publicacion descripcion
        @scrapes sitio time_stamp url 
        """
        l = ItemLoader(item=CodeworkersItem(), response=response)

        # Data de la oferta de empleo
        l.add_xpath('titulo', 'normalize-space(//h1[@class="aviso_title"])')
        l.add_xpath('empresa', 'normalize-space(//*[@id="empresa"])')
        l.add_xpath('ubicacion', 'normalize-space(//div[@class="aviso_specs"]/div[1]/div[@class="col-sm-12 col-md-6 col-lg-10 spec_def"]/a/text())')
        l.add_value('remoto', "sin informacion")
        l.add_xpath('tiempo_publicacion', '//*[@id="fechaPublicacion"]/@value',
            MapCompose(lambda i: datetime.datetime.strptime(i, "%d-%m-%Y")))
        l.add_xpath('descripcion', 'normalize-space(//div[@class="aviso_description"])')

        # Metadata de la oferta de empleo
        l.add_value('sitio', self.allowed_domains)
        l.add_value('marca_tiempo', datetime.datetime.now())
        l.add_value('url', response.url)
        self.item_count += 1
        if self.item_count > 5:
            raise CloseSpider('item_exceeded')
        return l.load_item()