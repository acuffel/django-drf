# Django DRF
Django DRF is an application to initialized project with Django and DRF using docker and docker-compose

## Installation

### Requirements
- [Docker](https://docs.docker.com/get-docker/): we use _Docker_ to develop and run __core__. This is a strict requirement to use this project.
- [Docker Compose](https://docs.docker.com/compose/install/): we use _Docker Compose_ to simplify the orchestration of all application services, using configuration files for different environments (such as _dev_, _test_, _staging_ or _prod_).

Download this repository and unzip it on your computer

Or clone the repository directly on your computer:
``` bash
$ git clone git@github.com:acuffel/django-drf.git
```

### Quickstart
To start the demo application, please run:
``` bash
$ make quickstart
```

Wait a bit for the application to build, then you can access it with your favorite internet browser to the following address: [http://localhost:8080](http://localhost:8080).

That's all!

There may be a conflict if port `8080` on your machine is already in use. In this case, you can change it with the following command with a suitable port number:
``` bash
$ NGINX_HOST_PORT=8080 make quickstart
```

To stop the demo application and remove all containers and volumes, please run:
``` bash
$ make stop
```

### Install and run a development environment
__core__ stores config in environment variables.
When using _Docker Compose_ to run __core__, the `.env` file is used to define all required environment variables.
You should never edit this `.env` file directly or store sensitive information in it, but you can override one or more of these variables by defining them directly in the shell before launching docker compose (values in the shell take precedence over those specified in the `.env` file.).

> **Notes for Windows users:**  
> You should set the following environment variable to enable path conversion from Windows-style to Unix-style in volume definitions:   
> `COMPOSE_CONVERT_WINDOWS_PATHS=1`

Once you have customized your environment variables, you can build and start a development environment with the following command:
``` bash
$ make dev
```

This previous command builds all the required services for development and starts them all except the _Django_ web server and workers.

#### _Django_ web server
To start the _Django_ web server, please open a terminal in the container:
``` bash
$ docker exec -it dev_core_1 /bin/bash
```

Then run:
``` bash
(core) $ cd /code/services/backend
(core) $ make collectstatic
(core) $ make migrate
(core) $ make populate-db
(core) $ make createsuperuser
(core) $ make runserver
```

#### _Celery_ workers
To start _Celery_ workers, please run in two different terminals:
``` bash
$ docker exec -it dev_core_1 make -C /code/services/backend worker-gateway
```
and:
``` bash
$ docker exec -it dev_core_1 make -C /code/services/backend worker-computation
```

### Exposed ports when using Docker Compose to run the application

| port      | service       | environment variable            | environment   | description                        |
| --------- | ------------- | ------------------------------- | ------------- | ---------------------------------- |
| __8080__  | reverse-proxy | `NGINX_HOST_PORT`               | `dev`, `demo` | NGINX server                       |
| 8081      | core          | `CORE_HOST_PORT_DEV`            | `dev`         | Django dev server                  |
| 5672      | broker        | `RABBITMQ_HOST_PORT_DEV`        | `dev`         | RabbitMQ server                    |
| __15672__ | broker        | `RABBITMQ_MANAGEMENT_HOST_PORT` | `dev`, `demo` | RabbitMQ management and monitoring |
| 5432      | core-db       | `POSTGRES_HOST_PORT_DEV`        | `dev`         | PostgreSQL server                  |
| 6379      | cache         | `REDIS_HOST_PORT_DEV`           | `dev`         | PostgreSQL server                  |
| 3000      | frontend      | `FRONTEND_HOST_PORT_DEV`        | `dev`         | Node dev server                    |

## Tech/framework used
- [NGINX](https://www.nginx.com/): a free and open-source web server used as a reverse proxy;
- [Django](https://www.djangoproject.com/): a Python-based free and open-source web framework;
- [Celery](https://docs.celeryproject.org/): Distributed Task Queue for Python;
- [PostgreSQL](https://www.postgresql.org/): a free and open-source relational database management system;
- [RabbitMQ](https://www.rabbitmq.com/): the most widely deployed open source message broker.

## Contributing
For the sake of simplicity, to ease interaction with the community, we use the [GitHub flow](https://guides.github.com/introduction/flow/index.html) for open-source projects. In a few words:
* The `main` branch is always stable and deployable;
* Tags from the `main` branch are considered as releases;
* Contributors have to fork or create a new feature-branch to work on (if they are allowed to in the original repository) and propose a pull request to merge their branch to `main`.

If you'd like to contribute, please raise an issue or fork the repository and use a feature branch. Pull requests are warmly welcome!

## Versioning
We use [SemVer](http://semver.org/) for versioning. See the [CHANGELOG.md](CHANGELOG.md) file for details.

## Licensing
The code in this project is licensed under MIT license. See the [LICENSE](LICENSE) file for details.
