################################################################################
# Docker and Docker Compose commands to be executed outside the container.     #
################################################################################

# Environment variables
# If the following required environment variables are not set,
# we try to get them from the .env file:

ifndef APP_NAME
	APP_NAME=$$(grep '^APP_NAME=' .env | cut -d= -f2-)
endif

ifndef CORE_DOCKER_IMAGE_NAME
	CORE_DOCKER_IMAGE_NAME=$$(grep '^CORE_DOCKER_IMAGE_NAME=' .env | cut -d= -f2-)
endif

ifndef CORE_DOCKER_IMAGE_VERSION
	CORE_DOCKER_IMAGE_VERSION=$$(grep '^CORE_DOCKER_IMAGE_VERSION=' .env | cut -d= -f2-)
endif

# Commands

default: help

.PHONY: clean-python
clean-python: ## Cleans Python environment.
	find . -path "*.pyc" -delete
	find . -path "*/__pycache__" -delete

.PHONY: build
build: clean-python ## Builds Docker image.
	docker build \
		--tag ${CORE_DOCKER_IMAGE_NAME}:${CORE_DOCKER_IMAGE_VERSION} \
		--tag ${CORE_DOCKER_IMAGE_NAME}:latest \
		--tag ${APP_NAME}/${CORE_DOCKER_IMAGE_NAME}:${CORE_DOCKER_IMAGE_VERSION} \
		--tag ${APP_NAME}/${CORE_DOCKER_IMAGE_NAME}:latest \
		--file services/backend/Dockerfile \
		.
	@echo "[ OK ] The '${APP_NAME}/${CORE_DOCKER_IMAGE_NAME}:${CORE_DOCKER_IMAGE_VERSION}' image was build successfully!"

.PHONY: quickstart
quickstart: build ## Builds Docker image and runs it in demo mode.
	docker-compose \
		--file docker-compose.yml \
		--project-name ${APP_NAME}_demo \
		up \
		--detach
	@echo "[ OK ] '${APP_NAME}_demo' is running on http://localhost:8080"
	@echo "[INFO] Please use 'make stop' to stop the running '${APP_NAME}_demo' application."

.PHONY: stop
stop: ## Stops the runing demo application.
	docker-compose \
		--file docker-compose.yml \
		--project-name ${APP_NAME}_demo \
		rm \
		--stop \
		--force \
		-v
	docker volume rm ${APP_NAME}_demo_brocker-data; exit 0
	docker volume rm ${APP_NAME}_demo_cache-data; exit 0
	docker volume rm ${APP_NAME}_demo_core-db-data; exit 0
	docker volume rm ${APP_NAME}_demo_core-media; exit 0
	docker volume rm ${APP_NAME}_demo_core-static; exit 0
	@echo "[ OK ] '${APP_NAME}_demo' is stopped and deleted."

.PHONY: dev
dev: clean-python ## Runs all services in development mode.
	mkdir -p services/backend/.tox
	mkdir -p services/backend/biodb
	mkdir -p services/backend/media
	mkdir -p services/backend/static
	mkdir -p services/backend/venv
	docker-compose \
		--file docker-compose.dev.yml \
		--project-name ${APP_NAME}_dev \
		up \
		--build \
		--remove-orphans \
		--renew-anon-volumes

.PHONY: tests
tests: ## Tests Docker image.
	docker exec -it ${APP_NAME}_dev_core_1 make -C /code/services/backend tests

.PHONY: clean-dev
clean-dev: clean-python ## Cleans development environment (Docker containers and volumes).
	docker rm ${APP_NAME}_dev_reverse-proxy_1; exit 0
	docker rm ${APP_NAME}_dev_core_1; exit 0
	docker rm ${APP_NAME}_dev_core-db_1; exit 0
	docker rm ${APP_NAME}_dev_brocker_1; exit 0
	docker rm ${APP_NAME}_dev_cache_1; exit 0
	docker volume rm ${APP_NAME}_dev_brocker-data; exit 0
	docker volume rm ${APP_NAME}_dev_cache-data; exit 0
	docker volume rm ${APP_NAME}_dev_core-db-data; exit 0
	docker volume rm ${APP_NAME}_dev_core-media; exit 0
	docker volume rm ${APP_NAME}_dev_core-static; exit 0
	docker volume rm ${APP_NAME}_dev_core-tox; exit 0
	docker volume rm ${APP_NAME}_dev_core-venv; exit 0
	rm -rf services/backend/.tox
	rm -rf services/backend/biodb
	rm -rf services/backend/media
	rm -rf services/backend/static
	rm -rf services/backend/venv

.PHONY: clean-dev-db
clean-dev-db: ## Cleans development databases (Docker containers and volumes).
	docker rm ${APP_NAME}_dev_core-db_1; exit 0
	docker rm ${APP_NAME}_dev_brocker_1; exit 0
	docker rm ${APP_NAME}_dev_cache_1; exit 0
	docker volume rm ${APP_NAME}_dev_brocker-data; exit 0
	docker volume rm ${APP_NAME}_dev_cache-data; exit 0
	docker volume rm ${APP_NAME}_dev_core-db-data; exit 0

.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
