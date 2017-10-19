FROM postgres
EXPOSE 5432
ENV DB_NAME codeworkers
ENV DB_USER postgres
ENV DB_PASS postgres
ADD setup-database.sh /docker-entrypoint-initdb.d/
RUN chmod 755 /docker-entrypoint-initdb.d/setup-database.sh

