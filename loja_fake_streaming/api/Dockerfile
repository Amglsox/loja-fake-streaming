# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

ENV POETRY_VERSION=1.2.2 \
  PORT=9090

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

ENV bootstrap_servers="<placeholder>:29092"
ENV topic_data="kafka-python-topic-person-official-2"

# Copy our Flask app to the Docker image
COPY app.py /code/
COPY . /code/
CMD gunicorn app:app -w 2 --threads 2 -b 0.0.0.0:${PORT}
