from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_puesto_trabajo_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class PuestoTrabajo(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "puesto_trabajo"

    id = Column(Integer, primary_key=True)
    titulo = Column('titulo', String)
    url = Column('url', String, nullable=True)
    location = Column('location', String, nullable=True)
    original_price = Column('original_price', Integer, nullable=True)
    price = Column('price', Integer, nullable=True)
    end_date = Column('end_date', DateTime, nullable=True) 
