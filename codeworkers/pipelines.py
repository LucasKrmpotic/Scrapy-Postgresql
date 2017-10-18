import datetime
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import CloseSpider, DropItem
from .models import OfertaEmpleo, db_connect, create_oferta_empleo_table


class CodeworkersPipeline(object):
    """Define los métodos para guardar los items en la db
    """
    def __init__(self):
 
        engine = db_connect()
        create_oferta_empleo_table(engine)
        self.Session = sessionmaker(bind=engine)

    def _compara_fechas(self, tiempo, fecha):
        return tiempo.year == fecha.year and tiempo.month == fecha.month and tiempo.day == fecha.day

    def process_item(self, item, spider):
        if self._compara_fechas(item['tiempo_publicacion'], item['marca_tiempo']):
            session = self.Session()
            puesto = OfertaEmpleo(**item)

            try:
                #import ipdb; ipdb.set_trace()
                session.add(puesto)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            return item
        else:
            raise DropItem()