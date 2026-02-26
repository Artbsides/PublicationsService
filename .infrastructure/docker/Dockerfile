FROM python:3.14.2-alpine AS development

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    pip install poetry-plugin-export

RUN poetry export --output requirements.txt --with-credentials --no-interaction
RUN poetry export --output requirements.dev.txt --with-credentials --no-interaction --with dev

RUN pip install -r requirements.dev.txt --require-hashes --no-cache-dir && \
    pip uninstall poetry --yes

COPY . .

ENV PYTHONPATH=/app

FROM python:3.14.2-alpine

WORKDIR /app

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

COPY --chown=appuser --from=development /app/requirements.txt .
COPY --chown=appuser --from=development /app/app ./app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --require-hashes --no-cache-dir

RUN rm requirements.txt

USER appuser

ENV APP_HOST=${APP_HOST:-0.0.0.0} \
    APP_HOST_PORT=${APP_HOST_PORT:-8000}

ENV PYTHONPATH=/app

CMD ["sh", "-c", "uvicorn app.main:app --host=${APP_HOST} --port=${APP_HOST_PORT} --workers=4 --loop uvloop --http httptools"]
