.ONESHELL:

SHELL  = /bin/bash
PYTHON = /usr/bin/python3


DOCKER_PATH = .infrastructure/docker


-include .env
export


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*?)(?: - (.*))?$$', line)
    if match:
        target, params, help = match.groups()
        target = target.ljust(21)
        params = params.ljust(55)
        print("  %s %s %s" % (target, params, help or ""))
endef
export PRINT_HELP_PYSCRIPT


MAKEFLAGS += --silent


help:
	@echo "Usage: make <command> <parameters>"
	@echo "Options:"

	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


build: stop  ## Build dockerized images, run tests and code convention
	@docker compose -f $(DOCKER_PATH)/compose.yaml build
	@docker compose -f $(DOCKER_PATH)/compose.yaml -f $(DOCKER_PATH)/compose.development.yaml build

	@$(MAKE) bucket
	@$(MAKE) database
	@$(MAKE) message-broker

# @$(MAKE) tests dockerized=true
# @$(MAKE) code-convention dockerized=true

bucket:  ## Run dockerized bucket message broker
	@docker compose --project-directory $(DOCKER_PATH) up minio minio-buckets --wait

database:  ## Run dockerized postgres database
	@docker compose --project-directory $(DOCKER_PATH) up postgres --wait

	@sleep 5
	@poetry run alembic upgrade head

message-broker:  ## Run dockerized rabbitmq message broker
	@docker compose --project-directory $(DOCKER_PATH) up rabbitmq --wait

run:  ## Run dockerized api - Parameters: dockerized=true
	@if [ "$(dockerized)" = "true" ]; then
		docker compose up api
	else
		poetry run uvicorn app.main:app --host $${APP_HOST:-127.0.0.1} --port $${APP_HOST_PORT:-8000} --reload
	fi

run-worker:  ## Run dockerized worker - Parameters: dockerized=true
	@if [ "$(dockerized)" = "true" ]; then
		docker compose up worker
	else
		poetry run celery -A workers.process_uploaded_file.app worker --loglevel=info --concurrency=2
	fi

%:
	@:
