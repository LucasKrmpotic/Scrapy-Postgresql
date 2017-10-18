import datetime
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.loader.processors import MapCompose, Join
from codeworkers.items import CodeworkersItem
from w3lib.html import remove_tags

class LaWebDelProgramadorSpider(CrawlSpider):
    """ Araña para extraer ofertas de trabajo del sitio lawebdelprogramador """
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

    def _parse_fecha(self, value):
        meses  = {
            'Enero': '01',
            'Febrero': '02',
            'Marzo': '03',
            'Abril': '04',
            'Mayo': '05',
            'Junio': '06',
            'Julio': '07',
            'Agosto': '08',
            'Septiembre': '09',
            'Octubre': '10',
            'Noviembre': '11',
            'Diciembre': '12'
        }
        patron = re.compile('.*(\d{2})(\s+)(de){1}(\s+)(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre)(\s+)(del){1}(\s+)(\d{4}).*')
        coincidencia = patron.findall(value)
        if coincidencia is not None:
            fecha_str = coincidencia[0][0] + '-'
            fecha_str = fecha_str + meses[coincidencia[0][4]] + '-'
            fecha_str = fecha_str + coincidencia[0][8]
            return datetime.datetime.strptime(fecha_str, "%d-%m-%Y")
        return datetime.datetime.now() - datetime.timedelta(days=3)

    def parse_item(self, response):
        """ Parsea propiedades de una página.

        @url https://www.lawebdelprogramador.com/trabajo/32-Argentina/index1.html
        @returns items 1
        @scrapes titulo ubicacion empresa tiempo_publicacion descripcion
        @scrapes sitio time_stamp url 
        """
        l = ItemLoader(item=CodeworkersItem(), response=response)

        # Data de la oferta de empleo
        l.add_xpath('titulo', '//h1/text()')
        l.add_xpath('empresa', 'normalize-space(//div[@class="ce listRow2 listRowJob newBlock"]/div[2]/div[1]/a/text())')
        l.add_xpath('ubicacion', '//table[@class="rowJobData"]/tbody/tr[1]/td[2]/text()')
        
        l.add_xpath('tiempo_publicacion', 'normalize-space(//div[@class="ce listRow2 listRowJob newBlock"]/div[2]/div[1])',
            MapCompose(lambda i: self._parse_fecha(i))
        )

        l.add_value('descripcion', 
            MapCompose(self.parse_descripcion(response, "//table/tbody/tr[3]/td[@colspan='2']"))
        )

        # Metadata de la oferta de empleo
        l.add_value('sitio', self.allowed_domains)
        l.add_value('marca_tiempo', datetime.datetime.now())
        l.add_value('url', response.url)
        self.item_count += 1
        if self.item_count > 25:
            raise CloseSpider('item_exceeded')
        return l.load_item()
