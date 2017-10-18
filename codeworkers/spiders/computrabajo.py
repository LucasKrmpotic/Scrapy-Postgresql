import datetime
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.loader.processors import Join, MapCompose
from codeworkers.items import CodeworkersItem

    
class CompuTrabajoSpider(CrawlSpider):
    """ Araña para extraer ofertas de trabajo del sitio computrabajo """

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

    def _parse_fecha(self, value):
        """ Si 'value' contiene la palabra 'hoy' retorna la fecha actual
            si no la contiene retorna una fecha anterior """
        return datetime.datetime.now() if re.match('.*(hoy|Hoy).*', value) else datetime.datetime.now() - datetime.timedelta(days=3)

    def parse_item(self, response):
        """ Parsea propiedades de una página.

        @url https://www.computrabajo.com.ar/trabajo-de-programador
        @returns items 1
        @scrapes titulo ubicacion empresa tiempo_publicacion descripcion
        @scrapes sitio time_stamp url 
        """
        l = ItemLoader(item=CodeworkersItem(), response=response)

        # Data de la oferta de empleo
        l.add_xpath('titulo', '//*[@id="MainContainer"]//h1/text()')
       
        l.add_xpath('empresa', 'normalize-space(//div[@class="plr15 pt10 pos_rel bWord divClick"]/a[@id="urlverofertas"]/text())')
        l.add_xpath('ubicacion', 'normalize-space(//section[@class="box box_r rOffer"]/ul/li[2]/span[2]/text())')
        l.add_value('remoto', "sin informacion")
        l.add_xpath('tiempo_publicacion', 'normalize-space(//section[@class="box box_r rOffer"]/ul/li[1]/span[2]/text())',
            MapCompose(lambda i: self._parse_fecha(i))
        )

        l.add_xpath('descripcion', 'normalize-space(//div[@class="cm-12 box_i"]/ul)',
            MapCompose(str.strip),
            Join()
        )

        # Metadata de la oferta de empleo
        l.add_value('sitio', self.allowed_domains)
        l.add_value('marca_tiempo', datetime.datetime.now())
        l.add_value('url', response.url)
        self.item_count += 1
        if self.item_count > 5:
            raise CloseSpider('item_exceeded')
        return l.load_item()
