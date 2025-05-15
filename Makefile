VENV = poetry run

APP = weasel
TESTS = tests


# CI/CD
cicd: format lint test


# Formatters
format: black

black:
	$(VENV) black $(APP) $(TESTS)


# Linters
lint: ruff mypy

mypy:
	$(VENV) mypy $(APP) $(TESTS)

ruff:
	$(VENV) ruff check $(APP) $(TESTS)


# Tests
test: unit-tests

unit-tests:
	$(VENV) pytest $(TESTS)
