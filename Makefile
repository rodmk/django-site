.PHONY: install-deps .install-deps venv runserver migrate test pre-commit type-check
.DEFAULT_GOAL = runserver

install-deps:
	uv sync --locked
	yarn install --frozen-lockfile

.install-deps:
	@make install-deps > /dev/null 2>&1 || exit 1

update-deps:
	uv update --locked
	yarn upgrade --latest

venv: .install-deps
	source .venv/bin/activate

runserver: .install-deps
	uv run python manage.py runserver

migrate: .install-deps
	uv run python manage.py migrate

test: .install-deps
	uv run python manage.py test

pre-commit: .install-deps
	pre-commit run --all-files

type-check: .install-deps
	uv run dmypy run -- .
