from scrapy.spiders import XMLFeedSpider
from codeworkers.items import CodeworkersItem
from scrapy.exceptions import CloseSpider
import datetime
import re

class MySpider(XMLFeedSpider):
    name = 'stackov2'
    allowed_domains = ["stackoverflow.com"]
    start_urls = ['https://stackoverflow.com/jobs/feed']
    iterator = 'iternodes'
    itertag = 'item'
    item_count = 0
    namespaces = [('a10', 'https://stackoverflow.com/jobs/feed')]

    def _parse_descripcion(self, descripcion):
        patron = re.compile('<.*?>')
        return re.sub(patron, '', str(descripcion))

    def _parse_fecha(self, fecha):
        meses  = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12'
        }
        patron = re.compile('.*(\d{2})(\s+)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\s+)(\d{4}).*')
        coincidencia = patron.findall(str(fecha))
        if coincidencia is not None:
            fecha_str = coincidencia[0][0] + '-'
            fecha_str = fecha_str + meses[coincidencia[0][2]] + '-'
            fecha_str = fecha_str + coincidencia[0][4]
            return datetime.datetime.strptime(fecha_str, "%d-%m-%Y")
        return datetime.datetime.now() - datetime.timedelta(days=3)

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))

        item = CodeworkersItem()
        item['titulo'] = node.xpath('title/text()').extract()
        item['empresa'] = node.xpath('//a10:author/a10:name/text()').extract()
        item['ubicacion'] = node.xpath('location/text()').extract()
        item['tiempo_publicacion'] = self._parse_fecha(node.xpath('pubDate/text()').extract_first())
        item['descripcion'] = self._parse_descripcion(node.xpath('description/text()').extract())
        item['sitio'] = self.allowed_domains
        item['marca_tiempo'] = datetime.datetime.now()
        item['url'] = node.xpath('link/text()').extract()
        self.item_count += 1
        if self.item_count > 5:
            raise CloseSpider('item_exceeded')
        return item
