#!/bin/sh

set -o errexit

# run the project's type checks
docker-compose -f local.yml run django mypy openfootprint
