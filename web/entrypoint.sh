#!/usr/bin/env bash
python manage.py db upgrade
python app.py -e prod
