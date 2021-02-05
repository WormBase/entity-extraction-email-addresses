FROM python:3.8-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /usr/src/app/
ADD requirements.txt .
RUN pip3 install -r requirements.txt
RUN python3 -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
COPY . .

ENV DB_HOST=""
ENV DB_NAME=""
ENV DB_USER=""
ENV DB_PASSWD=""
ENV MAX_NUM_PAPERS=50
ENV TAZENDRA_SSH_USER=""
ENV TAZENDRA_SSH_PASSWD=""

ADD crontab /etc/cron.d/email_ext-cron
RUN chmod 0644 /etc/cron.d/email_ext-cron
RUN touch /var/log/email_ext_pipeline.log
RUN crontab /etc/cron.d/email_ext-cron

ENV PYTHONPATH=$PYTHONPATH:/usr/src/app/

CMD echo $DB_HOST > /etc/email_ext_db_host && \
    echo $DB_NAME > /etc/email_ext_db_name && \
    echo $DB_USER > /etc/email_ext_db_user && \
    echo $DB_PASSWD > /etc/email_ext_db_passwd && \
    echo $MAX_NUM_PAPERS > /etc/email_ext_max_num_papers && \
    echo $TAZENDRA_SSH_USER > /etc/email_ext_tazendra_ssh_user && \
    echo $TAZENDRA_SSH_PASSWD > /etc/email_ext_tazendra_ssh_passwd && \
    cron && tail -f /dev/null