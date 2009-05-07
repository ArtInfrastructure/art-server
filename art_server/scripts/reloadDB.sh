#!/bin/bash

echo "drop database artserver; create database artserver; grant all on database artserver to postgres;" | psql -U postgres

python manage.py syncdb --noinput
python manage.py loaddata front/fixtures/sites.json
python manage.py loaddata front/fixtures/auth.json
python manage.py loaddata front/fixtures/front.json
python manage.py loaddata front/fixtures/artcam.json
echo "Done!"

