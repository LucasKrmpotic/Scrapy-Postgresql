# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import Join, MapCompose
from w3lib.html import remove_tags
import datetime

def parse_fecha(value):
    return datetime.datetime.strptime(value, "%d-%m-%Y")
    
    # datetime.datetime(fecha.year, fecha.month, fecha.day, tzinfo=datetime.timezone.utc)
    
class CodeworkersItem(Item):
    """ Define los atributos de un item
    """
    titulo =Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    ubicacion =Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    remoto = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    empresa = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    tiempo_publicacion = Field() 
    descripcion =Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )

    # Metadata de la oferta de empleo
    sitio =Field()
    marca_tiempo =Field()
    url =Field()