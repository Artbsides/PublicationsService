.ONESHELL:

SHELL  = /bin/bash
PYTHON = /usr/bin/python3


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

run:  ## Run dockerized api - Parameters: dockerized=true
	@if [ "$(dockerized)" = "true" ]; then
		docker compose up api
	else
		poetry run uvicorn app.main:app --host ${APP_HOST:-127.0.0.1} --port ${APP_HOST_PORT:-8000} --reload
	fi


%:
	@:
