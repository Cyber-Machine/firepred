FROM python:3.11-slim-buster

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /firepred

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR


# FROM python:3.11-slim-buster as runtime

# ENV VIRTUAL_ENV=/firepred/.venv \
#     PATH="/app/.venv/bin:$PATH"

# COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY models/randomForest.pkl ./models/randomForest.pkl
COPY firepred ./firepred

EXPOSE 5000
CMD ["poetry", "run", "python", "-m", "firepred"]