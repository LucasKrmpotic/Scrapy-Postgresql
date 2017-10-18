import datetime
import re
from urllib import parse
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from codeworkers.items import CodeworkersItem

    
class CompuTrabajoSpider(CrawlSpider):
    """ Araña para extraer ofertas de trabajo del sitio computrabajo """

    name = "computrabajo"
    item_count = 0
    allowed_domains = ["www.computrabajo.com.ar"]
    start_urls = (
        'https://www.computrabajo.com.ar/trabajo-de-programador',
    )
    
    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths='//li[@class="siguiente"]/a')),
    #     Rule(LinkExtractor(restrict_xpaths='//a[@class="js-o-link"]'),
    #          callback='parse_item')
    # )

    def _parse_fecha(self, value):
        """ Si 'value' contiene la palabra 'hoy' retorna la fecha actual
            si no la contiene retorna una fecha anterior """
        return datetime.datetime.now() if re.match('.*(hoy|Hoy).*', value) else datetime.datetime.now() - datetime.timedelta(days=3)
    
    def parse(self, response):
        # Get the next index URLs and yield Requests
        next_selector = response.xpath('//li[@class="siguiente"]/a//@href')
        for url in next_selector.extract():
            yield Request(parse.urljoin(response.url, url))

        # Iterate through products and create PropertiesItems
        selectors = response.xpath(
            '//div[@id="p_ofertas"]/div')
        for selector in selectors:
            yield self.parse_item(selector, response)

    def parse_item(self, selector, response):
        """ Parsea propiedades de una página.

        @url https://www.computrabajo.com.ar/trabajo-de-programador
        @returns items 1
        @scrapes titulo ubicacion empresa tiempo_publicacion descripcion
        @scrapes sitio time_stamp url 
        """
        l = ItemLoader(item=CodeworkersItem(), selector=selector)

        # Data de la oferta de empleo
        l.add_xpath('titulo', './/h2/a/text()')
       
        l.add_xpath('empresa', 'normalize-space(.//a[@class="empr"]/text())')
        l.add_xpath('ubicacion', './/span[@itemprop="addressLocality"]')
        
        l.add_xpath('tiempo_publicacion', './/span[@class="dO"]',
            MapCompose(lambda i: self._parse_fecha(i))
        ) 

        # Metadata de la oferta de empleo
        l.add_value('sitio', self.allowed_domains)
        l.add_value('marca_tiempo', datetime.datetime.now())
        l.add_xpath('url', './/h2/a/@href',
            MapCompose(lambda i: self.allowed_domains[0] + str(i))
        )
        self.item_count += 1
        if self.item_count > 5:
            raise CloseSpider('item_exceeded')
        return l.load_item()
