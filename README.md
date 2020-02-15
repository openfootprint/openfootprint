# OpenFootprint

Open source software for managing ecological footprint, including carbon emissions.

[![Gitter](https://img.shields.io/gitter/room/openfootprint/community.svg?style=flat-square)](https://gitter.im/openfootprint/community) [![Travis](https://img.shields.io/travis/openfootprint/openfootprint.svg)](https://travis-ci.org/openfootprint)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)](https://github.com/pydanny/cookiecutter-django/) 

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


## How to contribute

### Understand the architecture

OpenFootprint has a few main components:
 - A [Django app for the backend](https://github.com/openfootprint/openfootprint/tree/master/openfootprint/core)
 - A [Vue.js frontend](https://github.com/openfootprint/openfootprint/tree/master/frontend)
 - Some [default plugins](https://github.com/openfootprint/openfootprint/tree/master/plugins). You can easily add your own!

### Get in touch

[Join us on Gitter!](https://gitter.im/openfootprint/community)
