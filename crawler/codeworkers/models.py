from sqlalchemy import create_engine, Column, Integer, String, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from . import settings

DeclarativeBase = declarative_base()

def db_connect():
    """ Define la conexión con la base de datos.
    Para el trabajo con docker-compose solo hacer
    falta indicar en el atributo "host" del objeto 
    setings.DATABASE el mismo nombre dado al servicio
    db en el compose.yml"""
    return create_engine(URL(**settings.DATABASE))


def create_oferta_empleo_table(engine):
    """ Define la creación de la tabla si no existe
    """
    DeclarativeBase.metadata.create_all(engine)


class OfertaEmpleo(DeclarativeBase):
    """ Define los atributos de la tabla
    Esta clase debe ser consistente con la clase Item
    de Scrapy"""
    __tablename__ = "oferta_empleo"

    id = Column(Integer, primary_key=True)
    
    # Data de la oferta de empleo
    titulo = Column('titulo', String)
    ubicacion = Column('ubicacion', String, default="sin informacion")
    empresa = Column('empresa', String, nullable=True)
    tiempo_publicacion = Column('tiempo_publicacion', String)

    # Metadata de la oferta de empleo
    sitio = Column('sitio', String)
    marca_tiempo = Column('marca_tiempo', String)
    url = Column('url', String)
