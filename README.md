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
### En este proyecto se ha usado
* [Docker](https://www.docker.com/)
* [Postgresql](https://www.postgresql.org/)
* [Scrapy](https://scrapy.org/)
* [Cron](http://crontab.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [NodeJS](https://nodejs.org/es/)
* [node-postgres](https://node-postgres.com/)
