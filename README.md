# Codeworkers 
## Un proyecto para los laburantes del codigo

### Objetivo

La intención de este proyecto es poner en marcha una aplicación que permita a los programadores que buscan trabajar en Argentina, tener un sitio de referencia que centralice las ofertas de empleo naturalmente distribuidas en multiples sitios. 

La aplicacion simplemente muestra datos resumidos de las ofertas de empleo (título, empresa, ubicación, etc) y el link al sitio donde fue publicada originalmente a fin de poder acceder a sus datos detallados y eventualmente postularse y/o enviar CV.

### Estructura del proyecto

* **codeworkers (crawler)**

    Se encarga de extraer datos de ofertas de empleo para programadores de diferentes sitios web.

    Actualmente los siguientes:
    * bumeran.com.ar
    * computrabajo.com.ar
    * lawebdelprogramador.com
    * stackoverflow.com/jobs
    * zonajobs.com.ar

    [Detalles del crawler](/codeworkers/README.md)

* **api**

    Se encarga de gestionar los datos con los que el crawler va poblando la base de datos. 

    Por el momento su unica funcionalidad es mostrar todas las ofertas de trabajo o una en particular.

    [Detalles de la api](/api/README.md)

* **db**

    Define la construcción del contenedor de la base de datos.

    [Detalles de la db](/db/README.md)




