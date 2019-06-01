test:
	docker-compose -f local.yml run --rm django pytest

test_coverage:
	docker-compose -f local.yml run django coverage run -m pytest
	docker-compose -f local.yml run django coverage report

docker_build:
	docker-compose -f local.yml build

local_setup: docker_build migrate
	echo
	echo "Create your admin user:"
	docker-compose -f local.yml run --rm django python manage.py createsuperuser

local_webpack:
	docker-compose -f local.yml run --rm --service-ports webpack

devserver:
	docker-compose -f local.yml up

migrate:
	# docker-compose -f local.yml run --rm django python manage.py reset_schema
	docker-compose -f local.yml run --rm django python manage.py makemigrations
	docker-compose -f local.yml run --rm django python manage.py migrate

shell:
	docker-compose -f local.yml run --rm -ti django zsh
