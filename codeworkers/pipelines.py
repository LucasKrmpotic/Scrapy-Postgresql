from sqlalchemy.orm import sessionmaker
from .models import PuestoTrabajo, db_connect, create_puesto_trabajo_table


class CodeworkersPipeline(object):
 
    def __init__(self):
 
        engine = db_connect()
        create_puesto_trabajo_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        session = self.Session()
        puesto = PuestoTrabajo(**item)

        try:
            session.add(puesto)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
