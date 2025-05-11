FROM python:3.13-alpine3.21 AS production

WORKDIR /weasel/

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==2.1.2 \
    && poetry config virtualenvs.create false \
    && poetry install --no-ansi --no-interaction --no-root

COPY ./ ./

FROM production AS testing

RUN poetry install --no-ansi --no-interaction --no-root --with lint,test
