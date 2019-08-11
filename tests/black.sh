#!/bin/sh

set -o errexit

# Run black with --check option
docker-compose -f compose/local.yml run django black --check --diff  --exclude 'migrations' ./
