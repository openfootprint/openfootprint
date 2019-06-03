#!/bin/sh

set -o errexit

# run the project's type checks
docker-compose -f local.yml run django mypy openfootprint

# Run black with --check option
docker-compose -f local.yml run django black --check --diff  --exclude 'migrations' ./

# run the project's tests
docker-compose -f local.yml run django pytest . -v --junitxml=pytest-report.xml

# return non-zero status code if there are migrations that have not been created
docker-compose -f local.yml run django python manage.py makemigrations --dry-run --check || { echo "ERROR: there were changes in the models, but migration listed above have not been created and are not saved in version control"; exit 1; }
