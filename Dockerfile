FROM python
RUN apt-get update -q
COPY . .
RUN pip install -r requirements.txt
CMD ["bash", "cron-job.sh"] 

