FROM python:2

RUN mkdir -p /app
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN apt-get -y update \
    && apt-get -y install libmariadb-dev-compat git \
    && pip install -r ./requirements.txt

# Prepare files and folders so permissions will be set correctly once volumes are mounted
RUN mkdir -p /app/www/media
RUN mkdir -p /app/www/static
RUN chown -R www-data:www-data /app/www

RUN mkdir -p /app/log
RUN touch /app/log/info_log.log
RUN touch /app/log/error_log.log
RUN touch /app/log/sent_weekly_digests_log.txt
RUN touch /app/log/sent_daily_digests_log.txt
RUN chown -R www-data:www-data /app/log

# Copy code and setup
COPY ./entrypoint.sh /app
COPY ./uwsgi.ini /app
COPY ./web /app/web

RUN chmod +x /app/web/manage.py
RUN chmod +x /app/entrypoint.sh

RUN python ./web/manage.py collectstatic --noinput --settings=tutoring.settings_build

CMD ["./entrypoint.sh"]
