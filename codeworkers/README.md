## Crawler de ofertas de empleo para programadores

### Estructura del proyecto

* **codeworkers:** lógica del crawler
    * **spiders:** arañas para cada uno de los sitios
        * bumeran
        * computrabajo
        * lawebdelprogramador
        * stackoverflow
        * zonajobs
    * **items:** definición de los atributos a scrapear
    * **middlewares**
    * **models:** modelo para la base de datos
    * **pipelines:** procesamiento de un item
    * **settings**
* **crontab:** archivo crontab para el scrapeo programado
* **Dokerfile**
* **README**
* **requirements:** py dependencias del proyecto
* **scrapy-crawl:** scrip llamado en el crontab 
* **scrapy.cfg:** configuracion de Scrapy

    
