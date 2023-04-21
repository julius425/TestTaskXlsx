# This monolith Dockerfile:
# Uses FastAPI to serve static assets
# Uses gunicorn as a process manager to run the FastAPI app
WORKDIR /app

FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY backend/pyproject.toml backend/poetry.lock /app/

RUN poetry install --no-root

COPY backend /app

COPY --from=frontend-build /app/build /app/static

CMD gunicorn -k uvicorn.workers.UvicornWorker -b :8000 main:app
