################################################################################
# Python commands to be executed inside the container.                         #
################################################################################

default: help

.PHONY: venv
venv: ## Creates a virtual environment.
	python3 -m venv venv

.PHONY: install
install: ## Installs production dependencies.
	venv/bin/pip install --upgrade pip wheel setuptools
	venv/bin/pip install -r requirements.txt
	rm -rf ~/.cache/pip

.PHONY: requirements
requirements: ## Builds or updates requirements.
	venv/bin/pip install --upgrade pip wheel setuptools pip-tools
	venv/bin/pip-compile --upgrade requirements.in
	venv/bin/pip-compile --upgrade dev-requirements.in

.PHONY: install-dev
install-dev: ## Installs or updates development dependencies.
	venv/bin/pip install --upgrade pip wheel setuptools pip-tools
	venv/bin/pip-sync requirements.txt dev-requirements.txt

.PHONY: shell
shell: ## Starts the Django interactive interpreter.
	venv/bin/python manage.py shell

.PHONY: migrations
migrations: ## Creates new migrations based on the changes detected to your models.
	venv/bin/python manage.py makemigrations

.PHONY: migrate
migrate: ## Synchronizes the database state with the current set of models and migrations.
	venv/bin/python manage.py migrate

.PHONY: createsuperuser
createsuperuser: ## Creates a default superuser.
	venv/bin/python manage.py createsuperuser --no-input; exit 0

.PHONY: collectstatic
collectstatic: ## Collects the static files into STATIC_ROOT.
	venv/bin/python manage.py collectstatic --no-input --clear

.PHONY: runserver
runserver: ## Starts the Django development server.
	venv/bin/python manage.py runserver 0.0.0.0:8000

.PHONY: serve
serve: ## Starts the Gunicorn server.
	venv/bin/gunicorn myapp.wsgi:application

.PHONY: prod
prod: collectstatic migrate populate-db createsuperuser serve ## Starts Django in production mode.

.PHONY: demo
demo: collectstatic migrate populate-db createsuperuser runserver ## Starts Django in demo mode.

.PHONY: worker-gateway
worker-gateway: ## Starts the main Celery worker.
	venv/bin/celery -A myapp worker -n worker-gateway@%h -Q gateway

.PHONY: worker-computation
worker-computation: ## Starts a Celery worker for heavy computing tasks.
	venv/bin/celery -A myapp worker -n worker-computation@%h -Q computation

.PHONY: generate-secret-key
generate-secret-key: ## Generate a Secret Key.
	venv/bin/python utils/secret_key.py

.PHONY: tests
tests: ## Runs all tests.
	venv/bin/tox

.PHONY: tests-unit
tests-unit: ## Runs all unitary tests.
	venv/bin/python manage.py test

.PHONY: sleep
sleep: install-dev ## Installs development dependencies and wait.
	sleep infinity

.PHONY: clean-python
clean-python: ## Clean Python environment.
	find . -path "*.pyc" -not -path "./venv*" -delete
	find . -path "*/__pycache__" -not -path "./venv*" -delete

.PHONY: clean-migrations
clean-migrations: ## Remove all Django migrations.
	find . -path "*/migrations/*.py" -not -path "./venv*" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -not -path "./venv*" -delete

.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

