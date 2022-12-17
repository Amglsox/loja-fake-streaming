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

,PHONY: start-metabase
start-metabase: ## Start Metabase
	docker pull metabase/metabase:latest
	docker run -d -p 3000:3000 --name metabase metabase/metabase

,PHONY: stop-metabase
stop-metabase: ## Start Metabase
	docker stop metabase && docker rm metabase

.PHONY: kafka-start
start-kafka: ## Start Kafka
	cd ./kafka && docker-compose up -d

.PHONY: kafka-stop
stop-kafka: ## Stop Kafka
	cd ./kafka && docker-compose down --remove-orphans

.PHONY: api
start-api: ## Start api
	cd ./loja_fake_streaming/api/ && gunicorn app:app -w 2 --threads 2 -b 0.0.0.0:5050

.PHONY: build-api
build-api: ## Build API
	cp poetry.lock pyproject.toml ./loja_fake_streaming/api/ && cd ./loja_fake_streaming/api/ && docker build . -t loja-fake-api && rm -rf poetry.lock pyproject.toml

.PHONY: start-container-api
start-container-api: ## Start API
	docker run --name loja-fake --network kafka_default -d -p 9090:9090 loja-fake-api

.PHONY: down-container-api
down-container-api: ## Start API
	docker stop loja-fake && docker rm loja-fake

.PHONY: curl_druid
curl_druid: ##curl druid
	curl https://dlcdn.apache.org/druid/24.0.1/apache-druid-24.0.1-bin.tar.gz > ./apache-druid-24.0.1-bin.tar.gz

.PHONY: unzip_druid
unzip_druid: ##unzip druid
	tar -xzf ./apache-druid-24.0.1-bin.tar.gz -C ./

.PHONY: up_druid
up_druid: ##up-druid
	./apache-druid-24.0.1/bin/start-single-server-medium

.PHONY: start_druid
start_druid: curl_druid unzip_druid up_druid
