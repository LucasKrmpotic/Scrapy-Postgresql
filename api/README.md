# API para ofertas de empleos de programador
---
## Descripción

La aplicación consume datos de una base poblada por un crawler que extrae informacion referida a ofertas de empleo para programadores de 5 diferentes sitios web.

## Consideraciones sobre el [Dockerfile](Dockerfile)

Las imagenes mejor puntuadas de [DockerHub](https://hub.docker.com/), como [esta](https://hub.docker.com/r/google/nodejs/) contienen versiones de [node](https://nodejs.org/es/) anteriores a la [lts](https://nodejs.org/dist/latest-v6.x/docs/api/) por eso se optó por construir el contenedor a partir de la [imagen oficial de Debian](https://hub.docker.com/_/debian/).

Esto hace que el proceso sea un poco mas lento por lo que si se cuenta con alguna imagen que contenga [node^6.11.4](https://nodejs.org/es/) conviene editar el [Dockerfile](Dockerfile) a tales fines.

## Requisitos en caso de correr fuera del contenedor

 * [node^6.11.4](https://nodejs.org/es/)
 * [gulp y gulp-cli](https://gulpjs.com/)
 * [libnotify-bin](https://packages.debian.org/sid/libnotify-bin)

Correr con  
```
npm install && \
gulp
```

## Rutas disponibles (endpoints)

```
* localhost:3000/empleos
* localhost:3000/empleos/{id}
```

Para modificar las rutas en caso de querer probar la aplicación fuera de docker editar las siguientes lineas del archivo `router.js`

```javascript
    app.get('/empleos', listar);
    app.get('/empleos/:id', buscar)
```

Donde `listar` y `buscar` son los métodos de consulta a la base de datos

## Objeto empleo

    {
        'id': 
        'titulo':
        'ubicacion':
        'empresa':
        'sitio':
        'url':

    }

## Estructura del proyecto

```javascript
├── app
│   ├── app.js
│   ├── controllers
│   │   └── index_controller.js
│   ├── router.js
│   └── views
│       ├── error.jade
│       ├── index.jade
│       └── layout.jade
├── config
│   ├── config.json
│   └── env.js
├── Dockerfile
├── gulpfile.babel.js
├── package.json
├── README.md
└── server.js
```

El archivo `index_controller.js` contiene los métodos para consultas a la base de datos. Por ejemplo: 

```javascript
export function listar (req, res, next) {
    let pool = new Pool(pool_conf)
    pool.query('SELECT id, titulo, ubicacion, empresa, sitio, url FROM oferta_empleo')
      .then(result => res.json(result))
      .catch(e => console.error(e.stack))
    pool.end()
};
```

Donde `pool_conf` contiene los parametros que necesita el objeto pool de la librería [pg](https://www.npmjs.com/package/pg) (detalles sobre pg en [node-postgres](https://node-postgres.com/)).

```javascript
import $config from '../../config/config.json';
import { Pool } from 'pg';

let db = $config.db;
const pool_conf = {
  user: db.user,
  host: db.host,  
  database: db.database,
  password: db.password,
  port: db.port,
}
```

Para probar el funcionamiento de esta aplicación independientemente del ecosistema de contenedores de este proyecto editar en nodo `db` del archivo `config.json`

```javascript
"db": {
    "host": "db",
    "user": "postgres",
    "password": "postgres",
    "database": "codeworkers",
    "port": 5432
}
``` 
