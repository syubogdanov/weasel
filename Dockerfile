FROM python:3.13-alpine3.21 AS production

WORKDIR /weasel/

RUN apk add --no-cache \
    build-base \
    cargo \
    rust \
    cmake \
    musl-dev \
    libffi-dev \
    openssl-dev

COPY [ "./", "./" ]

RUN python -m pip install --no-cache-dir poetry==2.1.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-ansi --no-interaction

VOLUME [ "/tmp/" ]

ENTRYPOINT [ "poetry", "run", "weasel" ]
CMD [ "--help" ]
