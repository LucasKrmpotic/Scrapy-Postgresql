import datetime
import re
from urllib import parse
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from codeworkers.items import CodeworkersItem

class BumeranSpider(CrawlSpider):
    """ Araña para extraer ofertas de trabajo del sitio bumeran """

    name = "bumeran"
    item_count = 0
    terminar = False
    allowed_domains = ["www.bumeran.com.ar"]
    start_urls = (
        'http://www.bumeran.com.ar/empleos-busqueda-programador.html',
    )
    
    def _parse_fecha(self, cadena):
        """ Si 'cadena' contiene la palabra 'horas' o 'minutos' retorna la fecha actual
            si no la contiene retorna una fecha anterior """
        return datetime.datetime.now() if re.match('.*(horas|minutos).*', str(cadena)) else datetime.datetime.now() - datetime.timedelta(days=3)

    def parse(self, response):
        # Get the next index URLs and yield Requests
        next_selector = response.xpath('//ul[@class="pagination col-md-12"]/li[8]/a//@href')
        for url in next_selector.extract():
            yield Request(parse.urljoin(response.url, url))

        # Iterate through products and create PropertiesItems
        selectors = response.xpath(
            '//div[@class="list-jobs col-md-12 pd0"]/div/div')
        for selector in selectors:
            yield self.parse_item(selector, response)

    def parse_item(self, selector, response):
        """ Parsea propiedades de una página.

        @url http://www.bumeran.com.ar/empleos-busqueda-programador.html
        @returns items 1
        @scrapes titulo ubicacion empresa tiempo_publicacion descripcion
        @scrapes sitio time_stamp url 
        """
        l = ItemLoader(item=CodeworkersItem(), selector=selector)

        # Data de la oferta de empleo
        l.add_xpath('titulo', 'normalize-space(.//h3/text())')
        l.add_xpath('empresa', 'normalize-space(.//h4/text())')
        l.add_xpath('ubicacion', 'normalize-space(.//h5/text())')
        
        l.add_xpath('tiempo_publicacion', './/span[@class="fecha"]/text()',
            MapCompose(lambda i: self._parse_fecha(i)))

        # Metadata de la oferta de empleo
        l.add_value('sitio', self.allowed_domains)
        l.add_value('marca_tiempo', datetime.datetime.now())
        l.add_xpath('url', './/div/a[1]//@href',
            MapCompose(lambda i: self.allowed_domains[0] + str(i))
        )
        self.item_count += 1
        if self.item_count > 40:
            raise CloseSpider('item_exceeded')
        return l.load_item()


"""
//div[@class="list-jobs col-md-12 pd0"]/div/div[1]//span[@class="fecha
"""