VENV = poetry run


# CI/CD
cicd: format lint test


# Formatters
format: black

black:
	$(VENV) black ./


# Linters
lint: ruff mypy

mypy:
	$(VENV) mypy ./

ruff:
	$(VENV) ruff check ./


# Tests
test: unit-tests

unit-tests:
	$(VENV) pytest ./tests/
