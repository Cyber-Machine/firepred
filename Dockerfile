FROM python:3.11-buster

RUN pip install poetry==1.4.2

WORKDIR /firepred

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

COPY models/randomForest.pkl ./models/randomForest.pkl
COPY firepred ./firepred

EXPOSE 5000
CMD ["poetry", "run", "python", "-m", "firepred"]