#
# Dockerfile based on https://github.com/bmaingret/coach-planner/tree/main
#
ARG APP_NAME=mndot_bid
ARG APP_PATH=/opt/$APP_NAME
ARG PYTHON_VERSION=3.11.4
ARG POETRY_VERSION=1.5.1

#
# Stage: staging
#
FROM python:$PYTHON_VERSION as staging
ARG APP_NAME
ARG APP_PATH
ARG POETRY_VERSION

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install rclone
RUN curl https://rclone.org/install.sh | bash -

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

#
# Stage: production
#
FROM staging as production
ARG APP_NAME
ARG APP_PATH

WORKDIR $APP_PATH

# Install non-dev dependencies
COPY poetry.lock pyproject.toml .
RUN poetry install --no-root --no-directory --without dev

# Install project
COPY dbt/ ./dbt
COPY logs/ ./logs 
COPY scripts/ ./scripts
COPY src/ ./src
RUN poetry install --without dev

# Expose a volume mount point for persisting data between runs
# External data directory is not copied to keep image independent from data state
RUN mkdir ./data
VOLUME ./data

# Expose a volume mount point for the rclone config file
# Rclone expects the config at /root/.config/rclone/
RUN mkdir -p /root/.config/rclone/
VOLUME /root/.config/rclone/

# Expose a volume mount point for the rclone config file
VOLUME ./logs

# Set default shell for poetry
ENV SHELL=/bin/bash

# Install dbt plugins
RUN poetry run mndot-bid-cli dbt deps

ENTRYPOINT ["poetry", "run"]
CMD ["poetry", "shell"]
