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

# Import our project files
WORKDIR $APP_PATH
COPY poetry.lock pyproject.toml .

# Install core dependencies (not project, not dev dependencies)
RUN poetry install --no-root --without dev

#
# Stage: development
#
FROM staging as development
ARG APP_NAME
ARG APP_PATH

WORKDIR $APP_PATH

# Install project with dev dependencies
COPY . .
RUN poetry install

# Expose a volume mount point so that data is presisted between runs
VOLUME $APP_PATH/data

# Set default shell for poetry
ENV SHELL=/bin/bash

ENTRYPOINT ["poetry", "shell"]

#
# Stage: production
#
FROM staging as production
ARG APP_NAME
ARG APP_PATH

WORKDIR $APP_PATH

# Install project without development dependencies
COPY . .
RUN poetry install --without dev

# Expose a volume mount point so that data is presisted between runs
VOLUME $APP_PATH/data

# Set default shell for poetry
ENV SHELL=/bin/bash

RUN chmod +x ./scripts/update_prod_parquets.sh
ENTRYPOINT ["poetry", "run"]
CMD ["./scripts/update_prod_parquets.sh"]
