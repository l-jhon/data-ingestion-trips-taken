FROM python:3.9.7-slim-buster

# Environment variables
ENV POETRY_VERSION="1.1.13" \
    POETRY_VIRTUALENVS_CREATE=false \
    APP_DIR='/app' \
    POSTGRES_HOST="postgres_db" \
    POSTGRES_DB="trips" \
    POSTGRES_USER="trips" \
    POSTGRES_PASSWORD="password" \
    REDIS_URL="redis://redis:6379"

# Update packages
RUN apt-get update -y \
    && apt-get install -y build-essential python3-dev python3-setuptools curl \
    && pip install --upgrade --no-cache-dir pip \
    && curl -sSl https://install.python-poetry.org | python - --version "$POETRY_VERSION"

WORKDIR "$APP_DIR"

ADD resources "$APP_DIR/resources"
ADD src       "$APP_DIR/src"
ADD *.py      "$APP_DIR/"
ADD *.lock    "$APP_DIR/"
ADD *.toml    "$APP_DIR/"

# Installing project dependencies
RUN $HOME/.local/bin/poetry install --no-dev

# Run the project
CMD ["python", "$APP_DIR/main.py", "-h"]