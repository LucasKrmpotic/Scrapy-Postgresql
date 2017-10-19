import datetime
import re
from urllib import parse
from scrapy.loader.processors import MapCompose
from codeworkers.spiders.bumeran import BumeranSpider
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from codeworkers.items import CodeworkersItem

class ZonaJobsSpider(BumeranSpider):
    """ Araña para extraer ofertas de trabajo del sitio zonajobs """
    name = "zonajobs"
    allowed_domains = ["www.zonajobs.com.ar"]
    start_urls = (
        'https://www.zonajobs.com.ar/ofertas-de-trabajo-programador.html',
    )