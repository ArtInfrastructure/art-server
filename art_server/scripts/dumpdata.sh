#!/bin/bash

python manage.py dumpdata --indent=4 sites > front/fixtures/sites.json
python manage.py dumpdata --indent=4 auth > front/fixtures/auth.json
python manage.py dumpdata --indent=4 front > front/fixtures/front.json
python manage.py dumpdata --indent=4 artcam > front/fixtures/artcam.json

