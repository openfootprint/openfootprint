test:
	docker-compose -f local.yml run --rm django pytest

test_coverage:
	docker-compose -f local.yml run django coverage run -m pytest
	docker-compose -f local.yml run django coverage report

docker_build:
	docker-compose -f local.yml build

createsuperuser:
	echo
	echo "Create your admin user:"
	docker-compose -f local.yml run --rm django python manage.py createsuperuser


local_setup: docker_build migrate createsuperuser

local_webpack:
	docker-compose -f local.yml run --rm --service-ports webpack

devserver:
	docker-compose -f local.yml up

prodserver:
	docker-compose -f production.yml up

stopserver:
	docker-compose -f local.yml down || true
	docker-compose -f production.yml down || true
	docker-compose -f webpackbuildtest.yml down || true
	docker-compose -f utils.yml down || true

migrate:
	#
	docker-compose -f local.yml run --rm django python manage.py makemigrations
	docker-compose -f local.yml run --rm django python manage.py migrate

resetdb:
	docker-compose -f local.yml run --rm django python manage.py reset_schema
	docker-compose -f local.yml run --rm django python manage.py makemigrations core
	docker-compose -f local.yml run --rm django python manage.py migrate
	make createsuperuser

shell:
	docker-compose -f local.yml run --rm -ti django zsh

webpack_build:
	rm -rf frontend/webpack/prod/
	docker-compose -f utils.yml run --rm webpack_build_prod

webpack_build_test: webpack_build
	docker-compose -f webpackbuildtest.yml up