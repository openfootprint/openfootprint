# OpenFootprint

Open source software for managing ecological footprint, including carbon emissions.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)](https://github.com/pydanny/cookiecutter-django/)

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

[![Travis](https://img.shields.io/travis/openfootprint/openfootprint.svg)](https://travis-ci.org/openfootprint)

[![Join us on Slack](https://img.shields.io/badge/slack-join%20now-blue.svg?logo=slack)](https://join.slack.com/t/openfootprint/shared_invite/enQtNjQxMDAwNDcyMzIzLWZiYTk2YTlkZGUwNmNhNzgwMzE2N2ZhYmZjYzFhMDVjMTljYjc3YzdhODExYjllZDY3NjE1YjI4NTI4NDk2MmY)

License: Apache Software License 2.0

## Install

You must have Docker installed (https://docs.docker.com/install/). This is the only local dependency!

Then:

```
make local_setup
make devserver
```

Once the server is running, you can access your brand new install from your browser:
 - http://localhost:8700/ to start creating your first project
 - http://localhost:8700/admin/ to log into the Django admin panel (username: `admin`, password: `admin`)
 - http://localhost:8700/api/ for the REST API reference

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

## How to contribute

### Understand the architecture

OpenFootprint has a few main components:
 - A Django app for the backend.
 - A Vue.js frontend
 - Plugins