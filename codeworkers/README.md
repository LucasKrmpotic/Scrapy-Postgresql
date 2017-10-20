# Crawler de ofertas de empleo para programadores
---
## Descripción

La aplicación extrae informacion referida a ofertas de empleo para programadores de los siguientes sitios web:
* [bumeran.com.ar](bumeran.com.ar)
* [computrabajo.com.ar](computrabajo.com.ar)
* [lawebdelprogramador.com](lawebdelprogramador.com)
* [stackoverflow.com/jobs](stackoverflow.com/jobs)
* [zonajobs.com.ar](zonajobs.com.ar)

## Consideraciones sobre el [Dockerfile](Dockerfile)

Para cumplir el objetivo de extraer diariamente los datos *nuevos* de cada sitio se define una tarea [cron](http://crontab.org/) en el contenedor. Dicha tarea está definida en el archivo [scrapy-crawl.sh](scrapy-crawl.sh) y se encarga de lanzar las arañas segun el timestamp definido en el archivo [crontab](crontab).

En el archivo [Dockerfile](Dockerfile) se encuentra comentada la version que efectivamente cumple el objetivo y en su lugar se establece como comando (CMD) del contenedor un único llamado al script que lanza las arañas. Consistentemente con esto se encuentra comentada la linea de restart-policy en el archivo [docker-compose.yml](docker-compose.yml).

Por lo tanto, para probar la version con tareas programadas:

1. Remueva los contenedores si es que ya ejecutó `docker-compose up`
>docker-compose rm -f
2. Borre la imagen del crawler
>docker rmi scrapypostgresql_spiders
3. Defina el tiempo de la tarea en el archivo [crontab](crontab)
4. Descomente la linea `restart: unless-stopped` del archivo [docker-comose.yml](docker-compose.yml)

## Requisitos en caso de correr fuera del contenedor

 * [Python 3](https://www.python.org/downloads/release/python-363/)
 * [Virtualenv](https://virtualenv.pypa.io/en/stable/) y [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) (opcionales)

Correr con
```    
pip install -r requirements.txt && \
bash scrapy-crawl.sh
```

En virtualenv
```    
mkvirtualenv envname && \
workon envname && \
pip install -r requirements.txt && \
bash scrapy-crawl.sh
```

## Estructura del proyecto

```python
codeworkers
├── codeworkers
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── models.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       ├── bumeran.py
│       ├── computrabajo.py
│       ├── __init__.py
│       ├── lawebdelprogramador.py
│       ├── stackoverflow.py
│       └── zonajobs.py
├── crontab
├── Dockerfile
├── README.md
├── requirements.txt
├── scrapy.cfg
└── scrapy-crawl.sh

```

El archivo [models.py](codeworkers/models.py) contiene el código necesario para el trabajo con [SQLAlchemy](https://www.sqlalchemy.org/). 
El modelo define todos los atributos de la relación de tipo cadena para restar complejidad a la manipulacion de [items](codeworkers/item.py) en el trabajo con [Scrapy](https://scrapy.org/). 

```python
class OfertaEmpleo(DeclarativeBase):
    __tablename__ = "oferta_empleo"

    id = Column(Integer, primary_key=True)
    
    # Data de la oferta de empleo
    titulo = Column('titulo', String)
    ubicacion = Column('ubicacion', String, default="sin informacion")
    empresa = Column('empresa', String)
    tiempo_publicacion = Column('tiempo_publicacion', String)

    # Metadata de la oferta de empleo
    sitio = Column('sitio', String)
    marca_tiempo = Column('marca_tiempo', String)
    url = Column('url', String)
```
>Al atributo `ubicación` se le define un valor por defecto por no estar resuelto el parseo xpath en uno de los sitios.  

Nota:
>*Si bien el crawler trabaja con un ORM la api no, con lo cual no es trivial combiar el DBMS*.

En caso de querer crear la tabla `oferta_empleo` manualmente comentar la linea `create_oferta_empleo_table(engine)` en el constructor de la clase [CodeworkersPipeline](codeworkers/pipelines.py) encargada de la exportacion de los objetos [item](codeworkers/item.py) (docs sobre [ItemExporters](https://doc.scrapy.org/en/latest/topics/exporters.html)).

```python
def __init__(self):

    engine = db_connect()
    create_oferta_empleo_table(engine)
    self.Session = sessionmaker(bind=engine)
```

## Spiders
En virtud de los atributos definidos en el [modelo](codeworkers/models.py) y la estructura de los sitios web con los que se trabajó no fue necesario scrapear horizontalmente ya que toda la información se encontró en las páginas de índice.   

Por esto no se encontrarán reglas del tipo

```python
rules = {
    Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="pagination__next"]/a'))),
    Rule(LinkExtractor(allow =(), restrict_xpaths = ('//h2[contains(@class,"item__title")]/a')),
                        callback = 'parse_item')
}
```

En cambio se procesan varios items por cada *request*, con lo cual de cada *response* se extrae el *selector* que contiene la data y se procesa con en el método `parse_item`. Esto se logra redefiniendo el método `parse` propio de la araña genérica `CrawlSpider`.

```python
def parse(self, response):

    # Se obtiene la ruta a la siguiente página del índice
    next_selector = response.xpath('//ul[@class="pagination col-md-12"]/li[8]/a//@href')
    for url in next_selector.extract():
        yield Request(parse.urljoin(response.url, url))

    # Se itera por las instancias encontradas del selector objetivo
    selectors = response.xpath('//div[@class="list-jobs col-md-12 pd0"]/div/div')
    for selector in selectors:
        yield self.parse_item(selector, response)
```

