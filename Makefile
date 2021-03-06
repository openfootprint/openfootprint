test:
	docker-compose -f compose/local.yml run --rm django pytest

test_coverage:
	docker-compose -f compose/local.yml run django coverage run -m pytest
	docker-compose -f compose/local.yml run django coverage report

docker_build:
	docker-compose -f compose/local.yml build
	docker-compose -f compose/local.yml pull mailhog redis

createsuperuser:
	docker-compose -f compose/local.yml run --rm django python manage.py shell -c "exec('from django.contrib.auth import get_user_model\nUser = get_user_model()\nif not User.objects.filter(username=\"admin\").exists():\n User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin\")')"

lint: eslint
	docker-compose -f compose/local.yml run --rm --no-deps --entrypoint black django openfootprint
	docker-compose -f compose/local.yml run --rm --no-deps --entrypoint flake8 django openfootprint

eslint:
	docker-compose -f compose/utils.yml run --rm --no-deps --entrypoint node webpack_build_prod ../node_modules/eslint/bin/eslint.js --fix scripts/ scripts/**/*.*

pylint:
	docker-compose -f compose/local.yml run --rm --no-deps --entrypoint pylint django openfootprint

local_setup: docker_build migrate createsuperuser

local_webpack:
	docker-compose -f compose/local.yml run --rm --service-ports webpack

devserver:
	docker-compose -f compose/local.yml up

prodserver:
	docker-compose -f compose/production.yml up

stopserver:
	docker-compose -f compose/local.yml down || true
	docker-compose -f compose/production.yml down || true
	docker-compose -f compose/webpackbuildtest.yml down || true
	docker-compose -f compose/utils.yml down || true

migrate:
	#
	docker-compose -f compose/local.yml run --rm django python manage.py makemigrations
	docker-compose -f compose/local.yml run --rm django python manage.py migrate

resetdb:
	docker-compose -f compose/local.yml run --rm django python manage.py reset_schema
	docker-compose -f compose/local.yml run --rm django python manage.py makemigrations core
	docker-compose -f compose/local.yml run --rm django python manage.py migrate
	make createsuperuser

shell:
	docker-compose -f compose/local.yml run --rm django zsh

webpack_build:
	rm -rf frontend/webpack/prod/
	docker-compose -f compose/utils.yml run --rm webpack_build_prod

webpack_build_test: webpack_build
	docker-compose -f compose/webpackbuildtest.yml up