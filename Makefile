test:
	docker-compose -f compose/local.yml run --rm django pytest

test_coverage:
	docker-compose -f compose/local.yml run django coverage run -m pytest
	docker-compose -f compose/local.yml run django coverage report

docker_build:
	docker-compose -f compose/local.yml build

createsuperuser:
	echo
	echo "Create your admin user:"
	docker-compose -f compose/local.yml run --rm django python manage.py createsuperuser


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