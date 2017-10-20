FROM python
RUN apt-get update -q

RUN apt-get install -y cron

ADD scrapy-crawl.sh .
RUN chmod 750 scrapy-crawl.sh

ADD crontab /var/spool/cron/crontabs/root
RUN chmod 0600 /var/spool/cron/crontabs/root
RUN touch /var/log/scrapy-cron.log

COPY . .
RUN pip install -r requirements.txt

CMD ["cron", "&&", "tail", "-f", "/var/log/scrapy-cron.log"]

# para probar el funcionamiento inmediato de docker-compose up comentar 
# lineas anteriores y descomentar las siguientes

# FROM python
# RUN apt-get update -q
# ADD scrapy-crawl.sh .
# RUN chmod 750 scrapy-crawl.sh
# COPY . .
# RUN pip install -r requirements.txt
# CMD ["bash", "scrapy-crawl.sh"]
