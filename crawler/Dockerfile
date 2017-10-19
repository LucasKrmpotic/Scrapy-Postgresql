FROM python
RUN apt-get update -q
# RUN apt-get install -y cron
# RUN /etc/init.d/cron start > dev/null
COPY . /home
RUN pip install -r /home/requirements.txt

# Se definen las 11:00hs como hora de inicio del crawling
# RUN echo "0 11  * * * root /home/cron-job.sh" >> /etc/crontab 
# RUN /etc/init.d/cron restart

# para probar el funcionamiento inmediato de docker-compose up comentar 
# lineas anteriores y descomentar la siguiente
CMD ["bash", "/home/cron-job.sh"]
