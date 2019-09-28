#!/bin/sh

set -o errexit

# run the project's type checks
docker-compose -f compose/ci.yml run django mypy openfootprint
