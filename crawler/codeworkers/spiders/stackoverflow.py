import datetime
import re
from urllib import parse
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from codeworkers.items import CodeworkersItem

class StackOverflowSpider(CrawlSpider):
    """ Araña para extraer ofertas de trabajo del sitio stackoverflow """
    name = "stackoverflow"
    # item_count = 0
    allowed_domains = ["stackoverflow.com"]
    start_urls = (
        'https://stackoverflow.com/jobs',
    )

    def _parse_fecha(self, cadena):
        """ Si 'cadena' contiene la letra 'h' retorna la fecha actual
            si no la contiene retorna una fecha anterior """
        return datetime.datetime.now() if re.match('.*h+.*', str(cadena)) else datetime.datetime.now() - datetime.timedelta(days=3)
        

    def parse(self, response):
        
        next_selector = response.xpath('//a[@class="prev-next job-link test-pagination-next"]//@href')
        for url in next_selector.extract():
            yield Request(parse.urljoin(response.url, url))

        
        selectors = response.xpath(
            '//div[@class="listResults"]/div')
        for selector in selectors:
            yield self.parse_item(selector, response)

    def parse_item(self, selector, response):
        """ Parsea propiedades de una página.

        @url https://stackoverflow.com/jobs
        @returns items 1
        @scrapes titulo ubicacion empresa tiempo_publicacion
        @scrapes sitio marca_tiempo url 
        """
        l = ItemLoader(item=CodeworkersItem(), selector=selector)

        # Data de la oferta de empleo
        l.add_xpath('titulo', 'normalize-space(.//h2)')
        l.add_xpath('empresa', 'normalize-space(.//div[@class="-name"])')
        l.add_xpath('ubicacion', 'normalize-space(.//div[@class="-location"])')
        l.add_xpath('tiempo_publicacion', 'normalize-space(.//p[@class="-posted-date g-col"]/text())',
            MapCompose(lambda i: self._parse_fecha(i))
        )

        # Metadata de la oferta de empleo
        l.add_value('sitio', self.allowed_domains)
        l.add_value('marca_tiempo', datetime.datetime.now())
        l.add_xpath('url', './/h2/a//@href')

        # Para limitar la araña programaticamente descomentar estas lineas
        # (alternativa por linea de comandos añadir -s CLOSESPIDER_ITEMCOUNT=50) 
        # self.item_count += 1
        # if self.item_count > 50:
        #     raise CloseSpider('item_exceeded')
        # return l.load_item()