from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from . import settings

DeclarativeBase = declarative_base()

def db_connect():

    return create_engine(URL(**settings.DATABASE))


def create_puesto_trabajo_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class PuestoTrabajo(DeclarativeBase):

    __tablename__ = "puesto_trabajo"

    id = Column(Integer, primary_key=True)
    titulo = Column('titulo', String)
    url = Column('url', String, nullable=True)
