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

export function listar (req, res, next) {
    let pool = new Pool(pool_conf)
    pool.query('SELECT * FROM oferta_empleo')
      .then(result => res.json(result))
      .catch(e => console.error(e.stack))
    pool.end()
};

export function buscar (req, res, next) {
  let pool = new Pool(pool_conf)
  pool.query('SELECT * FROM oferta_empleo WHERE id = $1', [req.params.id])
    .then(result => res.json(result))
    .catch(e => console.error(e.stack))
    pool.end()
};