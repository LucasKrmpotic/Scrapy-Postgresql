## API para ofertas de empleos de programador

#### Endpoints

* localhost:3000/empleos
* localhost:3000/empleos/{id}

#### Objeto empleo

    {
        'id': 
        'titulo':
        'ubicacion':
        'empresa':
        'sitio':
        'url':

    }

#### Descripción

La aplicación consume datos de una base poblada por un crawler que extrae informacion referida a ofertas de empleo para programadores de 5 diferentes sitios web.

#### Estructura del proyecto

* **app:**
    * **controllers**
        * **index_controller.js:** metodos de consulta a la db
    * **views** 
    * **app.js:** aplicacion express con sus middlewares
    * **router.js:** declaración de los endpoints y controllers asociados
* **config**
    * **config.json:** env para la db y puerto a la escucha 
    * **env.js**
* **.babelrc:** configuracion del modulo babel para sintaxis EcmaScript 6
* **Dockerfile**
* **gulpfile.babel.js:** tareas gulp
* **packege.json**
* **README**
* **server.js:** registra uso de babel y llama a /app/app.js
 