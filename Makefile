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
	@docker compose -f $(DOCKER_PATH)/compose.yml build
	@docker compose -f $(DOCKER_PATH)/compose.yml -f $(DOCKER_PATH)/compose.development.yml build

	@$(MAKE) tests dockerized=true
	@$(MAKE) code-convention dockerized=true

dependencies:  ## Resolve dependencies for local development
	@poetry --version &> /dev/null || pip3 install poetry

	@poetry config virtualenvs.in-project true
	@poetry env use $(shell pyenv which python 2>/dev/null || which python3)

	@poetry lock
	@poetry install

tests: -B  ## Run tests - Parameters: dockerized=true, verbose=true
	POETRY_RUN=""
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker compose -f $(DOCKER_PATH)/compose.yml -f $(DOCKER_PATH)/compose.development.yml run -e APP_ENVIRONMENT=tests --rm shell"
	else
		POETRY_RUN="poetry run"
	fi

	APP_ENVIRONMENT=tests $$DOCKER_COMPOSE $$POETRY_RUN pytest $(if $(filter "$(verbose)", "true"),-sxvv,)

tests-debug: -B  ## Run debuggable tests - Parameters: dockerized=true, verbose=true
	POETRY_RUN=""
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker compose -f $(DOCKER_PATH)/compose.yml -f $(DOCKER_PATH)/compose.development.yml run -e APP_ENVIRONMENT=tests --service-ports --rm shell"
	else
		POETRY_RUN="poetry run"
	fi

	echo "==== Ready to attach to port 5789..."

	APP_ENVIRONMENT=tests PYDEVD_DISABLE_FILE_VALIDATION=true $$DOCKER_COMPOSE $$POETRY_RUN python \
		-m debugpy --listen ${APP_HOST}:5678 --wait-for-client -m pytest $(if $(filter "$(verbose)", "true"),-sxvv,)

coverage:  ## Run tests and write reports - Parameters: dockerized=true
	POETRY_RUN=""
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker compose -f $(DOCKER_PATH)/compose.yml -f $(DOCKER_PATH)/compose.development.yml run -e APP_ENVIRONMENT=tests --rm shell"
	else
		POETRY_RUN="poetry run"
	fi

	APP_ENVIRONMENT=tests $$DOCKER_COMPOSE $$POETRY_RUN pytest --cov-report=html:tests/reports

code-convention:  ## Run code convention - Parameters: dockerized=true, fix-imports=true, github=true
	POETRY_RUN=""
	DOCKER_COMPOSE=""

	@if [ "$(dockerized)" = "true" ]; then
		DOCKER_COMPOSE="docker compose -f $(DOCKER_PATH)/compose.yml -f $(DOCKER_PATH)/compose.development.yml run --rm shell"
	else
		POETRY_RUN="poetry run"
	fi

	$$DOCKER_COMPOSE $$POETRY_RUN ruff check . $(if $(filter "$(github)", "true"),--output-format github,)
	$$DOCKER_COMPOSE $$POETRY_RUN isort $(if $(filter "$(fix-imports)", "true"),,--check) . -q

storage:  ## Run dockerized storage message broker
	@docker compose -f $(DOCKER_PATH)/compose.yml up minio minio-buckets --detach

database:  ## Run dockerized postgres database
	@docker compose -f $(DOCKER_PATH)/compose.yml up postgres --wait

	@sleep 5
	@$(MAKE) database-migrations

database-migrations:  ## Run dockerized postgres database migrations
	@poetry run alembic upgrade head

message-broker:  ## Run dockerized rabbitmq message broker
	@docker compose -f $(DOCKER_PATH)/compose.yml up rabbitmq --wait

monitoring:  ## Run dockerized monitoring
	@docker compose -f $(DOCKER_PATH)/compose.yml up -d prometheus grafana loki tempo alloy --wait

run: database  ## Run api - Parameters: dockerized=true
	@if [ "$(dockerized)" = "true" ]; then
		docker compose -f $(DOCKER_PATH)/compose.yml up api
	else
		poetry run uvicorn app.main:app --host $${APP_HOST:-127.0.0.1} --port $${APP_PORT:-8000} --reload
	fi

run-development: database  ## Run debuggable dockerized api
	@COMPOSE_DEVELOPMENT_COMMAND="python -m debugpy --listen ${APP_HOST}:5678 -m uvicorn app.main:app --host ${APP_HOST} --port ${APP_PORT} --reload" \
		docker compose -f $(DOCKER_PATH)/compose.yml -f $(DOCKER_PATH)/compose.development.yml up api

run-worker:  ## Run worker - Parameters: dockerized=true
	@if [ "$(dockerized)" = "true" ]; then
		docker compose -f $(DOCKER_PATH)/compose.yml up worker
	else
		poetry run celery -A workers.create_publication.app worker --loglevel=info --concurrency=2
	fi

run-shell:  ## Run debuggable dockerized api terminal - Parameters: environment=staging|production
	SHELL="run --rm shell"

	@if [ "$(environment)" = "staging" ]; then
		docker compose -f $(DOCKER_PATH)/compose.yml -f $(DOCKER_PATH)/compose.development.yml $$SHELL
	elif [ "$(environment)" = "production" ]; then
		docker compose -f $(DOCKER_PATH)/compose.yml $$SHELL
	else
		echo "==== Environment not found."
	fi

stop:  ## Stop all dockerized services
	@docker compose -f $(DOCKER_PATH)/compose.yml down --volumes

secrets:  ## Encrypt or decrypt kubernetes secrets - Parameters: action=encrypt|decrypt, environment=staging|production
	@if [ "$(action)" = "encrypt" ]; then
		SECRETS_PATH=".infrastructure/kubernetes/$(environment)/secrets"
		SECRETS_PUBLIC_KEY="$$(cat $$SECRETS_PATH/.sops.yml | awk "/age:/" | sed "s/.*: *//" | xargs -d "\r")"

		sops -e -i --encrypted-regex "^(data|stringData)$$" -a $$SECRETS_PUBLIC_KEY \
			$$SECRETS_PATH/.secrets.yml

		echo "==== Ok"

	elif [ "$(action)" = "decrypt" ]; then
		SECRETS_KEY="$$(kubectl get secret sops-age --namespace argocd -o yaml | awk "/sops-age.txt:/" | sed "s/.*: *//" | base64 -d)"

		SOPS_AGE_KEY=$$SECRETS_KEY sops -d -i .infrastructure/kubernetes/$(environment)/secrets/.secrets.yml && \
			echo "==== Ok"

	else
		echo "==== Action not found."
	fi

github-tag:  ## Manage github tags - Parameters: action=create|delete, tag=[0-9].[0-9].[0-9]-staging|[0-9].[0-9].[0-9]
	@if [ "$(action)" = "create" ]; then
		git tag $(tag) && git push origin $(tag)
	elif [ "$(action)" = "delete" ]; then
		git tag -d $(tag) && git push origin :refs/tags/$(tag)
	else
		echo "==== Action not found"
	fi

%:
	@:
