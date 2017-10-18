import datetime

from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from codeworkers.items import CodeworkersItem

class StackOverflowSpider(CrawlSpider):
    """ Araña para extraer ofertas de trabajo del sitio stackoverflow """
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
        """ Parsea propiedades de una página.

        @url https://stackoverflow.com/jobs?med=site-ui&ref=jobs-tab
        @returns items 1
        @scrapes titulo ubicacion empresa tiempo_publicacion descripcion
        @scrapes sitio time_stamp url 
        """
        l = ItemLoader(item=CodeworkersItem(), response=response)

        l.add_xpath('titulo', '//h1[@class="-title"]/a/text()')

        l.add_xpath('empresa', '//a[@class="employer"]/text()')
        l.add_xpath('ubicacion', 'normalize-space(//div[@class="-location"]/text())')
        l.add_xpath('remoto', 'normalize-space(//div[@class="-perks g-row"]/p[2]/text())',
            MapCompose(lambda i: "Remoto" if re.match('.*(Remote).*', i) else "On site")
        )
        l.add_value('tiempo_publicacion', 'nada')

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
