# Detalles de la db

* DBMS [postgres](https://www.postgresql.org/)
* Docker [image](https://hub.docker.com/_/postgres/) 

Para setup de la base de datos se utilizó un script en bash que setea el servidor de base de datos utilizando las variables de ambiente que se le hayan pasado al momento de crear el contenedor. Esto es:

    POSTGRES_USER: usuario  
    POSTGRES_PASSWORD: password   
    POSTGRES_DB: la db de nuestro proyecto 

El código fue tomado de:

    https://github.com/macadmins/postgres/blob/master/setup-database.sh