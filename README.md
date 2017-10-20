# Codeworkers 
### Un proyecto para los laburantes del código

## Descripcion

La intención de este proyecto es poner en marcha un servicio que permita a los programadores que buscan trabajar en Argentina, tener un sitio de referencia que centralice las ofertas de empleo naturalmente distribuidas en multiples sitios. 

La aplicacion simplemente muestra datos resumidos de las ofertas de empleo (título, empresa, ubicación, etc) y el link al sitio donde fue publicada originalmente a fin de poder acceder a sus datos detallados y eventualmente postularse y/o enviar CV.

## Consideraciones sobre los contenedores

El proyecto consta de 3 contenedores, uno para cada uno de los siguientes servicios
* **Base de datos** - [Dockerfile](db/Dockerfile)
* **Crawler** - [Dockerfile](codeworkers/Dockerfile)
* **Api** - [Dockerfile](api/Dockerfile)

Correr con
>docker-conpose up

Luego en `localhost:3000/empleos` podrá chequear el funcionamiento del servicio (endpoints de la api [aquí](api/README.md))

### El contenedor de la api

Este contenedor corre una aplicación [NodeJS](https://nodejs.org/es/), sin embargo se parte de una [imagen oficial de Debian](https://hub.docker.com/_/debian/) para su construcción, por lo que puede demorar un poco ([vea los detalles](api/README.md)). 

### El contenedor del crawler

En el archivo [Dockerfile](codeworkers/Dockerfile) de este contenedor hay dos versiones para crear el servicio. Por la lógica del proyecto el crawling debe ejecutarse a intervalos regulares para lo que se utiliza [cron](http://crontab.org/). Sin embargo esto puede ser molesto para las pruebas de manera que por defecto el crawling se hará una sola vez y el contenedor morirá. 

Probar la versión más realista requiere mímimos cambios que se especifican [aquí](codeworkers/README.md) 


## Estructura del proyecto

```
├── api
│   ├── app
│   │   ├── app.js
│   │   ├── controllers
│   │   │   └── index_controller.js
│   │   ├── router.js
│   │   └── views
│   │       ├── error.jade
│   │       ├── index.jade
│   │       └── layout.jade
│   ├── config
│   │   ├── config.json
│   │   └── env.js
│   ├── Dockerfile
│   ├── gulpfile.babel.js
│   ├── package.json
│   ├── README.md
│   └── server.js
├── codeworkers
│   ├── codeworkers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── models.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │   └── spiders
│   │       ├── bumeran.py
│   │       ├── computrabajo.py
│   │       ├── __init__.py
│   │       ├── lawebdelprogramador.py
│   │       ├── stackoverflow.py
│   │       └── zonajobs.py
│   ├── crontab
│   ├── Dockerfile
│   ├── README.md
│   ├── requirements.txt
│   ├── scrapy.cfg
│   └── scrapy-crawl.sh
├── db
│   ├── Dockerfile
│   ├── README.md
│   └── setup-database.sh
├── docker-compose.yml
└── README.md

```
## Límites del proyecto
Algunas cuestiones de las que esta versión del proyecto no se ocupa son: 

1. No se han gestionado usuarios en los contenedores, ni en la db, ni se ha desarrollado esquema de autenticación y autorización y en la api.

2. No se controlan datos duplicados
    + Mas allá de mejorar esto en el crawler se debería incorporar procesamiento en la db para esto. Podría ser un trigger before ya que el crawler no debería esperar.

3. Si bien las arañas solo guardan datos de empleos que hayan sido publicados durante el día, no se ha resulelto del todo el problema de cuando parar. Por lo pronto cada araña tiene un limite fijo de items a scrapear con lo cual:
    * Si se publicaron menos ofertas que el límite se procesa de más (caso mas común)
    * Si se publicarom más ofertas se pierden datos
    * Además no en todos los sitios los datos se muestran ordenados de reciente a antiguo en orden de aparición
    * Todo esto limita la planificación de cron ya que si se ejecuta una sola vez al día es sumamente probable que se pierdan datos pero si se ejecuta más de una vez no hay duda de que habrá muchos datos duplicados (caso más común)

### En este proyecto se ha usado
* [Docker](https://www.docker.com/)
* [Postgresql](https://www.postgresql.org/)
* [Scrapy](https://scrapy.org/)
* [Cron](http://crontab.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [NodeJS](https://nodejs.org/es/)
* [node-postgres](https://node-postgres.com/)
