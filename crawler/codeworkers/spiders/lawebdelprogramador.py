import datetime
import re
from urllib import parse
from scrapy.loader.processors import MapCompose, Join
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from codeworkers.items import CodeworkersItem

class LaWebDelProgramadorSpider(CrawlSpider):
    """ Araña para extraer ofertas de trabajo del sitio lawebdelprogramador """
    name = "lawebdelprogramador"
    # item_count = 0
    allowed_domains = ["www.lawebdelprogramador.com"]
    start_urls = (
        'https://www.lawebdelprogramador.com/trabajo/32-Argentina/index1.html',
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

    def parse(self, response):
        # Get the next index URLs and yield Requests
        next_selector = response.xpath('//div[@class="pageb"]/a[6]//@href')
        for url in next_selector.extract():
            yield Request(parse.urljoin(response.url, url))

        # Iterate through products and create PropertiesItems
        selectors = response.xpath(
            '//div[@class="ce listRow2 listRowJob newBlock"]')
        for selector in selectors:
            yield self.parse_item(selector, response)

    def parse_item(self, selector, response):
        """ Parsea propiedades de una página.

        @url https://www.lawebdelprogramador.com/trabajo/32-Argentina/index1.html
        @returns items 1
        @scrapes titulo ubicacion empresa tiempo_publicacion descripcion
        @scrapes sitio time_stamp url 
        """
        l = ItemLoader(item=CodeworkersItem(), selector=selector)

        # Data de la oferta de empleo
        l.add_xpath('titulo', './/h2')
        l.add_xpath('empresa', 'normalize-space(./div[2]/div/a[1]/text())')
        l.add_xpath('ubicacion', './div/table/tbody/tr[1]/td[2]/text()',
            MapCompose(lambda i: "sin informacion" if not i else i)
        )
        
        l.add_xpath('tiempo_publicacion', 'normalize-space(./div[2]/div[1]/text())',
            MapCompose(lambda i: self._parse_fecha(i))
        )

        # Metadata de la oferta de empleo
        l.add_value('sitio', self.allowed_domains)
        l.add_value('marca_tiempo', datetime.datetime.now())
        l.add_xpath('url', './/h2/a/@href',
            MapCompose(lambda i: self.allowed_domains[0] + str(i))
        )
        # Para limitar la araña programaticamente descomentar estas lineas
        # (alternativa por linea de comandos añadir -s CLOSESPIDER_ITEMCOUNT=50) 
        # self.item_count += 1
        # if self.item_count > 50:
        #     raise CloseSpider('item_exceeded')
        # return l.load_item()