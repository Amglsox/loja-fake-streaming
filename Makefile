SHELL=/bin/bash

.DEFAULT_GOAL := help

.PHONY: help
help: ## Shows this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: init
init: clean install

.PHONY: clean
clean: ## Removes project virtual env
	rm -rf .venv build dist **/*.egg-info .pytest_cache node_modules .coverage

.PHONY: install
install: ## Install the project dependencies and pre-commit using Poetry.
	poetry install
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push


.PHONY: test
test: ## Run tests
	poetry run python -m pytest --cov=data_api_project --cov-report html

.PHONY: update
update: ## Run update poetry
	poetry update

,PHONY: metabase
start-metabase: ## Start Metabase
	docker pull metabase/metabase:latest
	docker run -d -p 3000:3000 --name metabase metabase/metabase

.PHONY: kafka
start-kafka: ## Start Kafka
	cd ./kafka && docker-compose up -d
