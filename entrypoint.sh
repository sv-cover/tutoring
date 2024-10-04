#!/usr/bin/env bash
python web/manage.py migrate --noinput
uwsgi --ini uwsgi.ini
