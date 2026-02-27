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


version:  ## Read or update app version - Parameters: update-to=[0-9].[0-9].[0-9]
	@poetry version $(if $(update-to), $(update-to), -s)

database:  ## Run dockerized postgres database - Parameters: seed=true
	@docker compose --project-directory $(DOCKER_PATH) up postgres --wait

	@if [ "$(seed)" = "true" ]; then
		$(MAKE) database-seeds
	fi

database-seeds:  ## Run seeds on dockerized postgres database - Parameters: dockerized=true
	POETRY_RUN=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker compose -f compose.yml -f compose.development.yml run --rm runner"
	else
		POETRY_RUN="poetry run"
	fi

	$$DOCKER_COMPOSE $$POETRY_RUN python seeds/main.py > /dev/null 2>&1 || true

bucket:  ## Run dockerized bucket message broker
	@docker compose --project-directory $(DOCKER_PATH) up minio minio-buckets --wait

message-broker:  ## Run dockerized rabbitmq message broker
	@docker compose --project-directory $(DOCKER_PATH) up rabbitmq --wait

run:  ## Run dockerized api - Parameters: dockerized=true
	@if [ "$(dockerized)" = "true" ]; then
		docker compose up api
	else
		poetry run uvicorn app.main:app --host $${APP_HOST:-127.0.0.1} --port $${APP_PORT:-8000} --reload
	fi


%:
	@:
