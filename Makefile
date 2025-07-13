# Makefile for setting up Python (uv) and JavaScript (yarn) dependencies

.PHONY: dev-setup
dev-setup:
	uv sync
	yarn install

.PHONY: runserver
runserver:
	@make dev-setup > /dev/null 2>&1 || exit 1
	uv run python manage.py runserver

.PHONY: migrate
migrate:
	@make dev-setup > /dev/null 2>&1 || exit 1
	uv run python manage.py migrate

.PHONY: test
test:
	@make dev-setup > /dev/null 2>&1 || exit 1
	uv run python manage.py test

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files
